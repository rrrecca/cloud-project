from flask import Blueprint, request, jsonify

extract_bp = Blueprint('extract', __name__)

@extract_bp.route('/pdf-a3/extract', methods=['POST'])
def extract_pdf():
    data = request.get_json()

    #  Basic validation
    if not data or 'pdfa3' not in data:
        return jsonify({
            "successful": False,
            "error": "Missing pdfa3 field"
        }), 400

    if 'content' not in data['pdfa3']:
        return jsonify({
            "successful": False,
            "error": "Missing pdfa3 content"
        }), 400

    pdf_base64 = data['pdfa3']['content']

    #  Temporary response (until A3 module is used)
    return jsonify({
        "successful": True,
        "attachments": [],
        "xml": {
            "content": "test_xml_base64",
            "mimeType": "application/xml",
            "filename": "metadata.xml"
        }
    }), 200