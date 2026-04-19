from flask import Blueprint, request, jsonify
import base64

generate_bp = Blueprint('generate', __name__)

print("✅ GENERATE FILE LOADED")

# 🔹 Utils Base64
def decode_base64(data):
    return base64.b64decode(data)

def encode_base64(data):
    return base64.b64encode(data).decode('utf-8')


@generate_bp.route('/pdf-a3/generate', methods=['POST'])
def generate_pdf():
    """
    Generate PDF/A-3 document
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
            - pdf
            - xml
          properties:
            pdf:
              type: object
              properties:
                content:
                  type: string
            xml:
              type: object
              properties:
                content:
                  type: string
            attachments:
              type: array
    responses:
      200:
        description: PDF/A-3 generated successfully
      400:
        description: Bad request
    """

    data = request.get_json()

    # 🔴 Validation
    if not data or 'pdf' not in data or 'xml' not in data:
        return jsonify({
            "successful": False,
            "error": "Missing required fields (pdf, xml)"
        }), 400

    try:
        pdf_bytes = decode_base64(data['pdf']['content'])
        xml_bytes = decode_base64(data['xml']['content'])

        attachments = []
        for att in data.get('attachments', []):
            attachments.append({
                "content": decode_base64(att['content']),
                "filename": att.get('filename'),
                "mimeType": att.get('mimeType')
            })

        return jsonify({
            "successful": True,
            "pdfa3": {
                "content": encode_base64(pdf_bytes)
            }
        }), 200

    except Exception as e:
        return jsonify({
            "successful": False,
            "error": str(e)
        }), 400