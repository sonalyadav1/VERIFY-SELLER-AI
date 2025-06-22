import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os
import sys

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        # Preprocessing: convert to grayscale, increase contrast, sharpen
        img = img.convert('L')
        img = ImageEnhance.Contrast(img).enhance(2.0)
        img = img.filter(ImageFilter.SHARPEN)
        text = pytesseract.image_to_string(img)
        print('OCR output:', text)
        sys.stdout.flush()
        return text
    except Exception as e:
        print('OCR error:', e)
        sys.stdout.flush()
        return ""
