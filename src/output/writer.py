import json
from pathlib import Path
from datetime import datetime
import cv2


def save_outputs(
    sample_id: int,
    lat: float,
    lon: float,
    decision: dict,
    area_sqm: float,
    bbox_or_mask,
    overlay_image,
    output_dir: Path,
    image_source: str = "ESRI"
):
    """
    Save JSON output and overlay image for a single sample.
    """

    json_dir = output_dir / "json"
    overlay_dir = output_dir / "overlays"

    json_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------
    # JSON payload
    # -------------------------------
    json_payload = {
        "sample_id": sample_id,
        "lat": lat,
        "lon": lon,
        "has_solar": decision["has_solar"],
        "confidence": decision["confidence"],
        "pv_area_sqm_est": area_sqm if decision["has_solar"] else 0.0,
        "buffer_radius_sqft": decision["buffer_radius_sqft"],
        "qc_status": decision["qc_status"],
        "bbox_or_mask": str(bbox_or_mask) if bbox_or_mask is not None else None,
        "image_metadata": {
            "source": image_source,
            "capture_date": datetime.now().strftime("%Y-%m-%d")
        }
    }

    json_path = json_dir / f"{sample_id}.json"
    with open(json_path, "w") as f:
        json.dump(json_payload, f, indent=2)

    # -------------------------------
    # Overlay image
    # -------------------------------
    if overlay_image is not None:
        overlay_path = overlay_dir / f"{sample_id}_overlay.png"
        cv2.imwrite(str(overlay_path), overlay_image)

    return json_path
