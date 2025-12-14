import numpy as np
from typing import List


def center_crop(image: np.ndarray, frac: float) -> np.ndarray:
    """
    Return a center crop of the image with given fractional size.
    frac = 1.0  -> full image
    frac = 0.75 -> tighter zoom
    frac = 0.5  -> strongest zoom
    """
    h, w, _ = image.shape
    crop_h = int(h * frac)
    crop_w = int(w * frac)

    y1 = (h - crop_h) // 2
    x1 = (w - crop_w) // 2

    return image[y1:y1 + crop_h, x1:x1 + crop_w]


def generate_multi_zoom_crops(image: np.ndarray) -> List[np.ndarray]:
    """
    Generate multi-zoom crops optimized for rooftop solar detection.

    Zoom levels:
      - Full image (context)
      - Medium center crop (0.75)
      - Tight center crop (0.5)

    This strategy improves detection of small PV installations
    in high-resolution satellite imagery.
    """
    zoom_fracs = [1.0, 0.75, 0.5]
    crops = []

    for frac in zoom_fracs:
        crops.append(center_crop(image, frac))

    return crops
