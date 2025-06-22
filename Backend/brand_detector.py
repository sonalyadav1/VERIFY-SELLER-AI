from rapidfuzz import fuzz
import os

LABELS_FILENAME = 'imagenet_labels.txt'
LABELS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), LABELS_FILENAME))

def load_brand_labels(labels_path=LABELS_PATH):
    if not os.path.exists(labels_path):
        raise FileNotFoundError(f"Brand labels file not found at {labels_path}. Please ensure the file is present.")
    with open(labels_path, 'r') as f:
        labels = [line.strip().lower() for line in f if line.strip()]
    return labels

# List of known brands (loaded from file)
KNOWN_BRANDS = load_brand_labels()

def detect_counterfeit_brand(input_brand, threshold=80):
    """
    Returns (is_counterfeit, best_match, score)
    is_counterfeit: True if input_brand is likely a misspelling/counterfeit
    best_match: Closest known brand
    score: Similarity score (0-100)
    """
    input_brand = input_brand.lower().strip()
    best_score = 0
    best_match = None
    for brand in KNOWN_BRANDS:
        score = fuzz.ratio(input_brand, brand)
        if score > best_score:
            best_score = score
            best_match = brand
    is_counterfeit = best_score < threshold
    return is_counterfeit, best_match, best_score
