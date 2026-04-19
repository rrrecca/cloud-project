from flask import Flask, request, jsonify
from flasgger import Swagger

from routes.generate import generate_bp
from routes.extract import extract_bp
from auth import validate_token

app = Flask(__name__)

# 🔐 Swagger config (Authorize button)
swagger = Swagger(app, template={
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Format: Bearer <your_token>"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
})

# 🔐 GLOBAL AUTH MIDDLEWARE
@app.before_request
def check_auth():

    # 🌐 Swagger + docs publics
    if (
        request.path.startswith("/apidocs")
        or request.path.startswith("/flasgger_static")
        or request.path.startswith("/static")
        or request.path == "/"
        or request.path == "/apispec_1.json"
    ):
        return None

    # 🔑 check token
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Missing token"}), 401

    if not validate_token(token):
        return jsonify({"error": "Invalid token"}), 403

    return None


# 📦 Blueprints
app.register_blueprint(generate_bp)
app.register_blueprint(extract_bp)


# 🌐 Public home
@app.route('/')
def home():
    return {"message": "PDF-A3 API is running"}


# 🧪 Test endpoint (protégé automatiquement)
@app.route("/test", methods=["GET"])
def test_route():
    """
    Test endpoint
    ---
    tags:
      - Auth
    responses:
      200:
        description: Token valid
        schema:
          type: object
          properties:
            message:
              type: string
    """
    return jsonify({"message": "token is valid"}), 200


if __name__ == "__main__":
    app.run(debug=True)