from flask import Blueprint, request, jsonify

generate_bp = Blueprint('generate', __name__)

@generate_bp.route('/pdf-a3/generate', methods=['POST'])
def generate_pdf():
    data = request.get_json()

    # 🔴 Basic validation
    if not data or 'pdf' not in data or 'xml' not in data:
        return jsonify({
            "successful": False,
            "error": "Missing required fields (pdf, xml)"
        }), 400

    if 'content' not in data['pdf'] or 'content' not in data['xml']:
        return jsonify({
            "successful": False,
            "error": "Missing content in pdf or xml"
        }), 400

    # 🟢 Extract fields
    pdf_base64 = data['pdf']['content']
    xml_base64 = data['xml']['content']
    attachments = data.get('attachments', [])
    lang = data.get('lang')
    afrelationship = data.get('afrelationship')

    # ⚠️ Temporary response (until A3 module is added)
    return jsonify({
        "successful": True,
        "pdfa3": {
            "content": pdf_base64  # just echo for now
        }
    }), 200