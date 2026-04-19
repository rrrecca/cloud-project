from flask import Blueprint, request, jsonify
import base64

extract_bp = Blueprint('extract', __name__)

print("✅ EXTRACT FILE LOADED")

# 🔹 Utils Base64
def decode_base64(data):
    return base64.b64decode(data)

def encode_base64(data):
    return base64.b64encode(data).decode('utf-8')


@extract_bp.route('/pdf-a3/extract', methods=['POST'])
def extract_pdf():
    """
    Extract PDF/A-3 document
    ---
    tags:
      - PDF-A3
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - pdfa3
          properties:
            pdfa3:
              type: object
              properties:
                content:
                  type: string
                  example: "base64-pdfa3"
    responses:
      200:
        description: Extraction successful
      400:
        description: Bad request
    """

    data = request.get_json()

    # 🔴 Validation
    if not data or 'pdfa3' not in data or 'content' not in data['pdfa3']:
        return jsonify({
            "successful": False,
            "error": "Missing pdfa3 content"
        }), 400

    try:
        pdf_bytes = decode_base64(data['pdfa3']['content'])

        # ⚠️ Simulation extraction
        extracted_xml = b"<xml>metadata</xml>"
        attachments = []

        return jsonify({
            "successful": True,
            "attachments": attachments,
            "xml": {
                "content": encode_base64(extracted_xml),
                "mimeType": "application/xml",
                "filename": "metadata.xml"
            }
        }), 200

    except Exception as e:
        return jsonify({
            "successful": False,
            "error": str(e)
        }), 400