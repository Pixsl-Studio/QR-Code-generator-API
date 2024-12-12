import io
import qrcode
from PIL import Image
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def create_transparent_qr(url):
    """
    Create a QR code with a transparent background
    """
    # Create QR code instance
    qr = qrcode.QRCode(
        version=None,  # Auto-size
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create the QR code image with a transparent background
    qr_img = qr.make_image(
        fill_color="black", 
        back_color="transparent"
    ).convert("RGBA")
    
    # Create a completely transparent background
    background = Image.new("RGBA", qr_img.size, (0, 0, 0, 0))
    
    # Alpha composite the QR code onto the transparent background
    transparent_qr = Image.alpha_composite(background, qr_img)
    
    return transparent_qr

@app.route('/generate-qr', methods=['POST'])
def generate_qr_code():
    """
    Generate a QR code with a transparent background from a provided URL
    """
    # Get URL from the request
    data = request.json
    if not data or 'url' not in data:
        return jsonify({"error": "URL is required"}), 400
    
    url = data['url']
    
    try:
        # Create QR code
        qr_img = create_transparent_qr(url)
        
        # Save to a bytes buffer
        img_byte_arr = io.BytesIO()
        qr_img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Send the file
        return send_file(
            img_byte_arr, 
            mimetype='image/png', 
            as_attachment=False
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

# Requirements:
# pip install flask flask-cors qrcode pillow
