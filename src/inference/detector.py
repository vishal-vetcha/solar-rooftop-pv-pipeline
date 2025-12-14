import numpy as np
from typing import Optional, Tuple, List


def run_multi_zoom_detection(
    model,
    crops: List[np.ndarray],
    conf_threshold: float = 0.25,
    imgsz: int = 1024,
    device: int = 0
) -> Tuple[bool, float, Optional[np.ndarray], Optional[Tuple[int, int, int, int]]]:
    """
    Run YOLO inference on multiple zoomed crops and aggregate results.

    Returns:
      has_solar (bool)
      best_confidence (float)
      best_mask (np.ndarray or None)
      best_bbox (tuple or None)
    """

    best_conf = 0.0
    best_mask = None
    best_bbox = None
    detected = False

    for crop in crops:
        # Safety check
        if crop is None or crop.size == 0:
            continue

        results = model(
            crop,
            conf=conf_threshold,
            imgsz=imgsz,
            device=device,
            verbose=False
        )

        if not results or results[0].boxes is None:
            continue

        boxes = results[0].boxes
        masks = results[0].masks

        if boxes is None or len(boxes) == 0:
            continue

        confs = boxes.conf.cpu().numpy()
        idx = int(np.argmax(confs))

        if confs[idx] > best_conf:
            best_conf = float(confs[idx])
            detected = True

            # Bounding box
            x1, y1, x2, y2 = boxes.xyxy[idx].cpu().numpy()
            best_bbox = (int(x1), int(y1), int(x2), int(y2))

            # Segmentation mask (if available)
            if masks is not None:
                best_mask = masks.data[idx].cpu().numpy().astype("uint8")
            else:
                best_mask = None

    return detected, best_conf, best_mask, best_bbox
