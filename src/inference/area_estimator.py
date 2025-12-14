import numpy as np
from src.utils.geo_utils import meters_per_pixel


def estimate_area_sqm(
    mask: np.ndarray,
    zoom: int
) -> float:
    """
    Estimate area (sqm) from segmentation mask.
    """

    if mask is None:
        return 0.0

    # Ensure binary mask
    binary_mask = (mask > 0).astype(np.uint8)

    pixel_count = int(binary_mask.sum())
    if pixel_count == 0:
        return 0.0

    mpp = meters_per_pixel(zoom)
    area_sqm = pixel_count * (mpp ** 2)

    return round(area_sqm, 2)
