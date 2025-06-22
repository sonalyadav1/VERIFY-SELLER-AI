from flask import Flask , request, jsonify
from flask_cors import CORS
import os
from model.predict import predict_fake
from brand_detector import detect_counterfeit_brand
from werkzeug.utils import secure_filename
from model.ocr_utils import extract_text_from_image
from model.logo_classifier import predict_logo

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image = request.files['image']
    temp_path = f"temp_{image.filename}"
    image.save(temp_path)
    
    # AI prediction
    risk, reason = predict_fake(temp_path)
    os.remove(temp_path)  # Clean up
    
    return jsonify({
        "risk": "high" if risk > 0.7 else "low",
        "reason": reason
    })

@app.route('/check_brand', methods=['POST'])
def check_brand():
    data = request.get_json()
    if not data or 'brand' not in data:
        return jsonify({'error': 'No brand provided'}), 400
    brand = data['brand']
    is_counterfeit, best_match, score = detect_counterfeit_brand(brand)
    return jsonify({
        'input_brand': brand,
        'is_counterfeit': is_counterfeit,
        'closest_brand': best_match,
        'similarity_score': score
    })

@app.route('/full_check', methods=['POST'])
def full_check():
    # Get form data
    brand = request.form.get('brand', '')
    price = request.form.get('price', type=float)
    address = request.form.get('address', '')
    account_age = request.form.get('account_age', type=int)
    listing_volume = request.form.get('listing_volume', type=int)
    image = request.files.get('image')

    # Always run OCR if image is present
    extracted_brand = None
    extracted_text = ''
    temp_path = None
    ocr_brand_result = None
    user_brand_result = None
    logo_result = None
    image_error = None
    try:
        if image:
            temp_path = secure_filename(f"temp_{image.filename}")
            image.save(temp_path)
            print('Calling OCR on:', temp_path)
            import sys
            sys.stdout.flush()
            extracted_text = extract_text_from_image(temp_path)
            print('Extracted text from image:', extracted_text)
            sys.stdout.flush()
            from brand_detector import KNOWN_BRANDS
            # Run counterfeit check on all words found by OCR
            words = [w for w in extracted_text.split() if w.isalpha()]
            best_score = 0
            best_word = ''
            best_match = ''
            is_counterfeit = False
            for word in words:
                c, match, score = detect_counterfeit_brand(word)
                if score > best_score:
                    best_score = score
                    best_word = word
                    best_match = match
                    is_counterfeit = c
            if best_word:
                extracted_brand = best_word
                ocr_brand_result = {
                    'is_counterfeit': is_counterfeit,
                    'closest_brand': best_match,
                    'similarity_score': best_score,
                    'source': 'image',
                    'extracted_text': extracted_text
                }
            # Logo classifier
            try:
                predicted_logo, logo_conf = predict_logo(temp_path)
                logo_result = {
                    'predicted_logo': predicted_logo,
                    'confidence': logo_conf
                }
            except Exception as e:
                logo_result = {'error': str(e)}
    except Exception as e:
        image_error = str(e)

    # User brand check (if provided)
    if brand:
        is_counterfeit, best_match, score = detect_counterfeit_brand(brand)
        user_brand_result = {
            'is_counterfeit': is_counterfeit,
            'closest_brand': best_match,
            'similarity_score': score,
            'source': 'user',
            'extracted_text': ''
        }

    # Image check
    image_result = None
    if image and temp_path and not image_error:
        risk, reason = predict_fake(temp_path)
        os.remove(temp_path)
        image_result = {
            'risk': 'high' if risk > 0.7 else 'low',
            'reason': reason
        }

    # Price check (simple: flag if price < 20 for expensive brands)
    price_result = None
    use_brand_for_price = brand or extracted_brand
    if price is not None and use_brand_for_price:
        suspicious = False
        reason = 'Normal price.'
        expensive_brands = ['nike', 'adidas', 'gucci', 'prada', 'louis vuitton', 'balenciaga']
        if use_brand_for_price.lower() in expensive_brands and price < 20:
            suspicious = True
            reason = 'Price too low for this brand.'
        price_result = {
            'suspicious': suspicious,
            'reason': reason
        }

    # Seller check (simple: flag if account is new and high volume or PO box)
    seller_result = None
    if account_age is not None and listing_volume is not None and address:
        risk = 'low'
        reason = 'Seller profile looks normal.'
        if account_age < 30 and listing_volume > 10:
            risk = 'high'
            reason = 'New account with high listing volume.'
        elif 'po box' in address.lower():
            risk = 'high'
            reason = 'PO box address detected.'
        seller_result = {
            'risk': risk,
            'reason': reason
        }

    response_data = {
        'user_brand_check': user_brand_result,
        'ocr_brand_check': ocr_brand_result,
        'logo_check': logo_result,
        'image_check': image_result,
        'price_check': price_result,
        'seller_check': seller_result,
        'image_error': image_error
    }
    print('API response:', response_data)
    import sys
    sys.stdout.flush()
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5050)