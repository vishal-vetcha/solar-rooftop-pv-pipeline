import argparse
from pathlib import Path

import cv2

from src.utils.config_loader import load_all_configs
from src.utils.logger import setup_logger

from src.data.excel_loader import load_input_excel
from src.data.image_fetcher import fetch_esri_image

from src.inference.model_loader import load_model
from src.inference.multi_zoom import generate_multi_zoom_crops
from src.inference.detector import run_multi_zoom_detection
from src.inference.area_estimator import estimate_area_sqm

from src.qc.qc_logic import apply_qc_logic
from src.utils.image_utils import overlay_mask, overlay_bbox
from src.output.writer import save_outputs


def main(input_excel: str, output_dir: str):
    # -------------------------------
    # Setup
    # -------------------------------
    logger = setup_logger()
    logger.info("Pipeline started")

    settings, model_cfg = load_all_configs()

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------
    # Load input data
    # -------------------------------
    df = load_input_excel(input_excel)
    logger.info(f"Loaded {len(df)} samples from Excel")

    # -------------------------------
    # Load model
    # -------------------------------
    model = load_model(model_cfg)
    logger.info("Model loaded successfully")

    # -------------------------------
    # Process each sample
    # -------------------------------
    for _, row in df.iterrows():
        sample_id = int(row["sample_id"])
        lat = float(row["latitude"])
        lon = float(row["longitude"])

        logger.info(f"Processing sample_id={sample_id}")

        # ---------------------------
        # Fetch image
        # ---------------------------
        image = fetch_esri_image(
            lat=lat,
            lon=lon,
            image_size=settings["image_source"]["image_size_px"]
        )

        image_available = image is not None
        overlay_img = None
        best_mask = None
        best_bbox = None
        area_sqm = 0.0

        # Default buffer
        buffer_sqft = settings["buffer_policy"]["fallback_buffer_sqft"]

        detected = False
        confidence = 0.0

        if image_available:
            # ---------------------------
            # Multi-zoom inference
            # ---------------------------
            crops = generate_multi_zoom_crops(image)

            detected, confidence, best_mask, best_bbox = run_multi_zoom_detection(
                model=model,
                crops=crops,
                conf_threshold=model_cfg["inference"]["conf_threshold"],
                imgsz=640,
                device=0
            )

            # If detected, use primary buffer
            if detected:
                buffer_sqft = settings["buffer_policy"]["primary_buffer_sqft"]

                # Estimate area (assume zoom=19)
                if best_mask is not None:
                    area_sqm = estimate_area_sqm(best_mask, zoom=19)

                # Create overlay
                if best_mask is not None:
                    overlay_img = overlay_mask(
                        image,
                        best_mask,
                        alpha=settings["output"]["overlay_alpha"]
                    )
                elif best_bbox is not None:
                    overlay_img = overlay_bbox(image, best_bbox)

        # ---------------------------
        # QC decision
        # ---------------------------
        decision = apply_qc_logic(
            image_available=image_available,
            detected=detected,
            confidence=confidence,
            buffer_radius_sqft=buffer_sqft,
            min_confidence=settings["inference"]["min_confidence_verifiable"]
        )

        # ---------------------------
        # Save outputs
        # ---------------------------
        save_outputs(
            sample_id=sample_id,
            lat=lat,
            lon=lon,
            decision=decision,
            area_sqm=area_sqm,
            bbox_or_mask=best_bbox if best_bbox else best_mask,
            overlay_image=overlay_img,
            output_dir=output_dir
        )

        logger.info(
            f"Completed sample_id={sample_id} | "
            f"has_solar={decision['has_solar']} | "
            f"qc={decision['qc_status']}"
        )

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solar Rooftop PV Detection Pipeline")

    parser.add_argument(
        "--input",
        required=True,
        help="Path to input Excel file (.xlsx)"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path to output directory"
    )

    args = parser.parse_args()

    main(args.input, args.output)
