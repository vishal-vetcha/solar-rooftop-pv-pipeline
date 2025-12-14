def apply_qc_logic(
    image_available: bool,
    detected: bool,
    confidence: float,
    buffer_radius_sqft: int,
    min_confidence: float
) -> dict:
    """
    Apply QC rules to inference result.
    """

    # Case 1: No image
    if not image_available:
        return {
            "has_solar": False,
            "confidence": 0.0,
            "buffer_radius_sqft": buffer_radius_sqft,
            "qc_status": "NOT_VERIFIABLE"
        }

    # Case 2: Detection with sufficient confidence
    if detected and confidence >= min_confidence:
        return {
            "has_solar": True,
            "confidence": round(confidence, 3),
            "buffer_radius_sqft": buffer_radius_sqft,
            "qc_status": "VERIFIABLE"
        }

    # Case 3: Image exists but detection is weak or absent
    return {
        "has_solar": False,
        "confidence": round(confidence, 3),
        "buffer_radius_sqft": buffer_radius_sqft,
        "qc_status": "NOT_VERIFIABLE"
    }
