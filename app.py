import io
import qrcode
from PIL import Image
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


def create_transparent_qr(url: str) -> Image.Image:
    """
    Create a QR code with a transparent background.

    :param url: The URL to encode in the QR code.
    :return: PIL Image object with a transparent background QR code.
    """
    # Create QR code instance
    qr = qrcode.QRCode(
        version=None,  # Auto-adjust size
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,  # Size of each QR box
        border=4,  # Default border
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create the QR code image
    qr_img = qr.make_image(fill_color="black", back_color=None).convert("RGBA")

    # Ensure background is fully transparent
    transparent_background = Image.new("RGBA", qr_img.size, (0, 0, 0, 0))
    transparent_qr = Image.alpha_composite(transparent_background, qr_img)

    return transparent_qr


@app.route('/generate-qr', methods=['POST'])
def generate_qr_code():
    """
    API endpoint to generate a QR code with a transparent background.
    Accepts a JSON payload with a "url" key.
    """
    # Parse JSON payload
    try:
        data = request.json
        if not data or 'url' not in data:
            return jsonify({"error": "Missing 'url' in the request payload"}), 400

        url = data['url']
        if not isinstance(url, str) or not url.strip():
            return jsonify({"error": "'url' must be a non-empty string"}), 400
    except Exception as e:
        return jsonify({"error": "Invalid JSON payload", "details": str(e)}), 400

    try:
        # Generate QR code
        qr_img = create_transparent_qr(url)

        # Save image to a byte stream
        img_byte_arr = io.BytesIO()
        qr_img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Return the image as a response
        return send_file(
            img_byte_arr,
            mimetype='image/png',
            as_attachment=False
        )

    except Exception as e:
        return jsonify({"error": "Failed to generate QR code", "details": str(e)}), 500


if __name__ == '__main__':
    # Run the app in production-safe mode
    app.run(debug=False, host='0.0.0.0', port=5000)
