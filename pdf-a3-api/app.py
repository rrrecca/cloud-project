from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)

# تكوين Swagger
app.config['SWAGGER'] = {
    'title': 'PDF A3 API',
    'openapi': '3.0.2'
}

swagger = Swagger(app)

@app.route('/pdf-a3/generate', methods=['POST'])
def generate_pdf():
    """Generate PDF A3
    ---
    post:
      summary: Generate PDF document
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: string
      responses:
        200:
          description: Success
    """
    data = request.get_json()
    return jsonify({
        'success': True,
        'message': 'PDF generated',
        'data': data.get('data') if data else None
    })

@app.route('/pdf-a3/extract', methods=['POST'])
def extract_pdf():
    """Extract from PDF
    ---
    post:
      summary: Extract data from PDF
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                pdf_base64:
                  type: string
      responses:
        200:
          description: Success
    """
    data = request.get_json()
    return jsonify({
        'success': True,
        'message': 'Data extracted',
        'has_pdf': data.get('pdf_base64') is not None if data else False
    })

@app.route('/')
def home():
    return jsonify({'message': 'API is running', 'docs': '/apidocs/'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)