# Dummy predict_fake function for prototype
# Replace with your actual model logic if available

def predict_fake(image_path):
    """
    Simulate AI prediction for fake product detection.
    Returns (risk_score, reason)
    """
    # For demo: if filename contains 'fake', return high risk
    if 'fake' in image_path.lower():
        return 0.9, 'Logo/image appears suspicious.'
    return 0.2, 'No obvious signs of counterfeiting.'
