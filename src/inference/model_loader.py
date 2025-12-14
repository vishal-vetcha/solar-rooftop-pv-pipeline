from ultralytics import YOLO
from pathlib import Path
import torch


def load_model(model_config: dict):
    """
    Load YOLOv8 segmentation model based on config.
    """
    weights_path = Path(model_config["model"]["weights_path"])

    if not weights_path.exists():
        raise FileNotFoundError(f"Model weights not found: {weights_path}")

    model = YOLO(str(weights_path))

    device = model_config["model"].get("device", "cpu")
    if device == "cuda" and torch.cuda.is_available():
        model.to("cuda")
    else:
        model.to("cpu")

    return model
