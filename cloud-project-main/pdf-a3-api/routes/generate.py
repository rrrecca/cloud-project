from flask import Blueprint, request, jsonify
import base64

generate_bp = Blueprint('generate', __name__)

# 🔹 Utils Base64
def decode_base64(data):
    return base64.b64decode(data)

def encode_base64(data):
    return base64.b64encode(data).decode('utf-8')

# 🔹 Fake JWT verification (à remplacer par JWKS plus tard)
def verify_token(auth_header):
    if not auth_header or not auth_header.startswith("Bearer "):
        return False
    return True

@generate_bp.route('/generate', methods=['POST'])
def generate_pdf():
    """
    Generate PDF/A-3 document
    ---
    tags:
      - PDF-A3
    security:
      - Bearer: []
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
                  example: "base64-pdf"
            xml:
              type: object
              properties:
                content:
                  type: string
                  example: "base64-xml"
            lang:
              type: string
              example: "en-US"
            afrelationship:
              type: string
              example: "Source"
            attachments:
              type: array
              items:
                type: object
                properties:
                  content:
                    type: string
                  mimeType:
                    type: string
                  filename:
                    type: string
    responses:
      200:
        description: PDF/A-3 generated successfully
      400:
        description: Bad request
      401:
        description: Unauthorized
    """
    """
    # 🔐 Auth
    auth_header = request.headers.get("Authorization")
    if not verify_token(auth_header):
        return jsonify({
            "successful": False,
            "error": "Unauthorized"
        }), 401
    """
    data = request.get_json()

    # 🔴 Validation
    if not data or 'pdf' not in data or 'xml' not in data:
        return jsonify({
            "successful": False,
            "error": "Missing required fields"
        }), 400

    try:
        # 🟢 Decode
        pdf_bytes = decode_base64(data['pdf']['content'])
        xml_bytes = decode_base64(data['xml']['content'])

        # 📎 Attachments
        attachments = []
        for att in data.get('attachments', []):
            attachments.append({
                "content": decode_base64(att['content']),
                "filename": att.get('filename'),
                "mimeType": att.get('mimeType')
            })

        # ⚠️ Simulation A3 (remplacé plus tard)
        result_pdf = pdf_bytes

        return jsonify({
            "successful": True,
            "pdfa3": {
                "content": encode_base64(result_pdf)
            }
        }), 200

    except Exception as e:
        return jsonify({
            "successful": False,
            "error": str(e)
        }), 400