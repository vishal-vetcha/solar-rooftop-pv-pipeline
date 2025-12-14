import cv2
import numpy as np


def overlay_mask(
    image: np.ndarray,
    mask: np.ndarray,
    color=(0, 255, 0),
    alpha: float = 0.45
) -> np.ndarray:
    """
    Overlay a single binary mask on image.
    """
    overlay = image.copy()
    colored_mask = np.zeros_like(image)
    colored_mask[mask > 0] = color

    cv2.addWeighted(colored_mask, alpha, overlay, 1 - alpha, 0, overlay)
    return overlay


def overlay_bbox(
    image: np.ndarray,
    bbox,
    color=(0, 255, 0),
    thickness: int = 2
) -> np.ndarray:
    """
    Draw bounding box on image.
    bbox = (x1, y1, x2, y2)
    """
    x1, y1, x2, y2 = map(int, bbox)
    img = image.copy()
    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
    return img


def overlay_multiple_masks(
    image: np.ndarray,
    masks: list,
    color=(0, 255, 0),
    alpha: float = 0.45
) -> np.ndarray:
    """
    Overlay multiple segmentation masks.
    """
    output = image.copy()
    for mask in masks:
        output = overlay_mask(output, mask, color=color, alpha=alpha)
    return output
