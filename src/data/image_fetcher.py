import requests
import numpy as np
from PIL import Image
from io import BytesIO

def fetch_esri_image(lat, lon, size=1024):
    url = "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export"

    # Progressive bbox expansion (robust)
    deltas = [0.002, 0.004, 0.006]

    for delta in deltas:
        params = {
            "bboxSR": 4326,
            "imageSR": 3857,
            "bbox": f"{lon-delta},{lat-delta},{lon+delta},{lat+delta}",
            "size": f"{size},{size}",
            "format": "png",
            "f": "image"
        }

        try:
            r = requests.get(url, params=params, timeout=30)

            if "image" not in r.headers.get("Content-Type", ""):
                continue

            img = Image.open(BytesIO(r.content)).convert("RGB")
            return np.array(img)

        except Exception:
            continue

    return None
