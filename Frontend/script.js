async function checkFraud() {
  const file = document.getElementById('product-image').files[0];
  const formData = new FormData();
  formData.append('image', file);

  const response = await fetch('http://localhost:5050/predict', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  document.getElementById('risk-score').textContent = result.risk;
  document.getElementById('reason').textContent = result.reason;
  
  // Highlight risk
  document.getElementById('result').className = 
    result.risk === 'high' ? 'high-risk' : 'low-risk';
}

async function checkBrand() {
  const brandInput = document.getElementById('brand-name').value;
  if (!brandInput) {
    alert('Please enter a brand name.');
    return;
  }
  const response = await fetch('http://localhost:5050/check_brand', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ brand: brandInput })
  });
  const result = await response.json();
  const brandResult = document.getElementById('brand-result');
  if (result.error) {
    brandResult.textContent = result.error;
    brandResult.className = '';
    return;
  }
  if (result.is_counterfeit) {
    brandResult.textContent = `Suspicious brand! Closest match: ${result.closest_brand} (score: ${result.similarity_score})`;
    brandResult.className = 'high-risk';
  } else {
    brandResult.textContent = `Brand looks genuine. Closest match: ${result.closest_brand} (score: ${result.similarity_score})`;
    brandResult.className = 'low-risk';
  }
}

async function runAllChecks(event) {
  if (event) event.preventDefault();
  try {
    const file = document.getElementById('product-image').files[0];
    const brand = document.getElementById('brand-name').value;
    const price = document.getElementById('product-price').value;
    const address = document.getElementById('seller-address').value;
    const accountAge = document.getElementById('account-age').value;
    const listingVolume = document.getElementById('listing-volume').value;

    // Prevent submitting if both brand and image are empty
    if (!file && !brand) {
      document.getElementById('all-results').innerHTML = `<span style="color:red;">Please upload an image or enter a brand name.</span>`;
      return;
    }

    const formData = new FormData();
    if (file) formData.append('image', file);
    formData.append('brand', brand);
    formData.append('price', price);
    formData.append('address', address);
    formData.append('account_age', accountAge);
    formData.append('listing_volume', listingVolume);

    console.log('Submitting formData:', { hasFile: !!file, brand, price, address, accountAge, listingVolume });
    const response = await fetch('http://localhost:5050/full_check', {
      method: 'POST',
      body: formData
    });
    console.log('Received response:', response);
    if (!response.ok) {
      throw new Error('Server error: ' + response.status);
    }
    const result = await response.json();
    console.log('Parsed result:', result);
    let html = '';
    html += `<pre style='background:#f4f4f4;padding:8px;border-radius:4px;'>${JSON.stringify(result, null, 2)}</pre>`;
    if (result.user_brand_check) {
      html += `<p><b>User Brand:</b> <span class="${result.user_brand_check.is_counterfeit ? 'high-risk' : 'low-risk'}">${result.user_brand_check.is_counterfeit ? 'Suspicious' : 'Genuine'} (Closest: ${result.user_brand_check.closest_brand}, Score: ${result.user_brand_check.similarity_score})</span></p>`;
    }
    if (result.ocr_brand_check) {
      html += `<p><b>Detected from Image:</b> <span class="${result.ocr_brand_check.is_counterfeit ? 'high-risk' : 'low-risk'}">${result.ocr_brand_check.is_counterfeit ? 'Suspicious' : 'Genuine'} (Closest: ${result.ocr_brand_check.closest_brand}, Score: ${result.ocr_brand_check.similarity_score})</span></p>`;
      html += `<p style='font-size:0.95em;color:#0071ce;'>Extracted text: <b>${result.ocr_brand_check.extracted_text || '(no text found)'}</b></p>`;
    }
    if (!result.user_brand_check && !result.ocr_brand_check) {
      if (result.logo_check && result.logo_check.predicted_logo && result.logo_check.predicted_logo !== 'unknown') {
        html += `<p><b>Logo Classifier:</b> <span class="${result.logo_check.confidence > 0.5 ? 'low-risk' : 'high-risk'}">${result.logo_check.predicted_logo} (Confidence: ${(result.logo_check.confidence * 100).toFixed(1)}%)</span></p>`;
      } else {
        html += `<p style='color:#d7263d;'>No brand detected from image. Please enter a brand name or upload a clearer image.</p>`;
      }
    }
    if (result.image_check) {
      html += `<p>Image: <span class="${result.image_check.risk === 'high' ? 'high-risk' : 'low-risk'}">${result.image_check.risk} risk</span> (${result.image_check.reason})</p>`;
    }
    if (result.price_check) {
      html += `<p>Price: <span class="${result.price_check.suspicious ? 'high-risk' : 'low-risk'}">${result.price_check.suspicious ? 'Suspicious' : 'Normal'} (${result.price_check.reason})</span></p>`;
    }
    if (result.seller_check) {
      html += `<p>Seller: <span class="${result.seller_check.risk === 'high' ? 'high-risk' : 'low-risk'}">${result.seller_check.risk} risk</span> (${result.seller_check.reason})</p>`;
    }
    if (result.logo_check && result.logo_check.error) {
      html += `<p><b>Logo Classifier:</b> <span style='color:#d7263d;'>Error: ${result.logo_check.error}</span></p>`;
    }
    if (result.image_error) {
      html += `<p style='color:red;'><b>Image processing error:</b> ${result.image_error}</p>`;
    }
    document.getElementById('all-results').innerHTML = html;
  } catch (err) {
    console.error('Error in runAllChecks:', err);
    document.getElementById('all-results').innerHTML = `<span style="color:red;">Error: ${err.message}</span>`;
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const btn = document.getElementById('run-fraud-btn');
  if (btn) {
    btn.addEventListener('click', function(event) {
      runAllChecks(event);
    });
  }
});