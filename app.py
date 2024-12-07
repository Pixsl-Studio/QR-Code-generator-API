from flask import Flask, request, send_file, jsonify
import qrcode
from qrcode.image.svg import SvgPathImage
import io

app = Flask(__name__)

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    # Get the input URL from the query parameters
    input_url = request.args.get('url', 'https://example.com')  # Default if no URL provided
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0,  # No white border
    )
    qr.add_data(input_url)
    qr.make(fit=True)

    # Generate a transparent QR code image
    img = qr.make_image(fill_color="black", back_color=None)  # Transparent background

    # Save to in-memory file in PNG format
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Prepare the downloadable file link
    response = send_file(
        buffer,
        mimetype="image/png",
        as_attachment=True,
        download_name="qr_code.png"
    )

    return response

if __name__ == '__main__':
    app.run(debug=True)
