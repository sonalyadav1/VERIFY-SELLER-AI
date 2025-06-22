# Verify Seller AI

Verify Seller AI is a web application designed to detect counterfeit sellers and fake branded products using Optical Character Recognition (OCR), logo classification, and risk analysis.

---

## 🚀 Features

- **OCR Analysis:** Extracts and analyzes text from product images to assess authenticity.
- **Logo Classification:** Uses deep learning to detect and verify brand logos.
- **Risk Analysis:** Evaluates products and sellers for potential fraud based on image and textual data.
- **Simple Frontend:** User-friendly web interface for uploading product details and images.

---

## 📂 Project Structure

```
Backend/
  app.py
  brand_detector.py
  imagenet_labels.txt
  mobilenetv2-7.onnx
  requirements.txt
  model/
    logo_classifier.py
    ocr_utils.py
    predict.py
  Data/
    Test/
    Train/
    Fake/
    Real/
Frontend/
  index.html
  script.js
  style.css
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```sh
git clone <https://github.com/sonalyadav1/VERIFY-SELLER-AI.git>
cd VERIFY-SELLER-AI
```

### 2. Backend Setup

a. **Create a virtual environment (recommended):**

```sh
cd Backend
python3 -m venv .venv
source .venv/bin/activate
```

b. **Install dependencies:**

```sh
pip install -r requirements.txt
```

c. **Model & Label Files:**

Ensure the following files are present in `Backend/`:
- `mobilenetv2-7.onnx` (ONNX model for logo classification)
- `imagenet_labels.txt` (brand labels, one per line)

d. **Run the backend server:**

```sh
python app.py
```

### 3. Frontend Setup

No build step is required. Simply open `Frontend/index.html` in your browser.

> **Note:** The backend server must be running for full functionality.

---

## 💻 Usage

1. Open `Frontend/index.html` in your browser.
2. Fill in product details and/or upload an image.
3. Click **"Run Fraud Checks"** to perform risk analysis and brand verification.

---

## 🛠 Troubleshooting

- **Missing Python packages:**  
  Install any missing packages using `pip install <package>`.
- **Backend not running:**  
  Ensure you have started the backend server before using the frontend.
- **OCR/Logo detection errors:**  
  Confirm that `pytesseract`, `onnxruntime`, and all required model files are installed and accessible.

---

## 📄 License

MIT License

---

## 👩‍💻 Authors

- Sonal Yadav

## 🤝 Collaborators

<!-- Add collaborator names here -->
