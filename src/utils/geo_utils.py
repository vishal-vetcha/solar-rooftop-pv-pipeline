import math


# ===============================
# Unit Conversions
# ===============================

def sqft_to_sqm(area_sqft: float) -> float:
    return area_sqft * 0.092903


def sqm_to_sqft(area_sqm: float) -> float:
    return area_sqm / 0.092903


# ===============================
# Buffer Radius Logic
# ===============================

def buffer_radius_meters(area_sqft: float) -> float:
    """
    Given buffer area in sq.ft, return radius in meters
    assuming circular buffer.
    """
    area_sqm = sqft_to_sqm(area_sqft)
    return math.sqrt(area_sqm / math.pi)


# ===============================
# Image Scale Logic
# ===============================

def meters_per_pixel(zoom: int) -> float:
    """
    Approx meters per pixel at equator.
    """
    zoom_to_mpp = {
        18: 0.597,
        19: 0.298,
        20: 0.149
    }
    return zoom_to_mpp.get(zoom, 0.298)


def pixel_radius_from_buffer(area_sqft: float, zoom: int) -> int:
    """
    Convert buffer area (sq.ft) to pixel radius for cropping.
    """
    radius_m = buffer_radius_meters(area_sqft)
    mpp = meters_per_pixel(zoom)
    return int(radius_m / mpp)
