from flask import Flask, request, jsonify
import qrcode
from io import BytesIO
import os

app = Flask(__name__)

# Temporary local file storage path
UPLOAD_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    input_url = request.args.get('url', 'https://example.com')  # URL to encode
    
    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0
    )
    qr.add_data(input_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color=None)  # Transparent QR

    # Save the QR code to a local PNG file
    file_name = f"qr_{input_url.replace('https://', '').replace('http://', '').replace('/', '_')}.png"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    img.save(file_path, format="PNG")

    # Generate a public URL (if hosted on Render or a similar platform)
    public_url = f"https://your-app-name.onrender.com/{file_path}"

    # Return the public URL
    return jsonify({"qr_code_url": public_url})

if __name__ == '__main__':
    app.run(debug=True)
