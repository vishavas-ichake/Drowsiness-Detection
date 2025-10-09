def validate_landmarks(landmarks, required_indices):
    """Check if all required landmark indices exist."""
    if landmarks is None:
        return False
    for idx in required_indices:
        if idx >= len(landmarks):
            return False
    return True
