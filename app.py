from flask import Flask, request, send_file
import qrcode
import io

app = Flask(__name__)

@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    data = request.json.get("url")
    if not data:
        return {"error": "Missing 'url' in the request body"}, 400

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code to an in-memory buffer
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name="qrcode.png")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
