
from flask import Flask
from flasgger import Swagger
from routes.generate import generate_bp
from routes.extract import extract_bp

app = Flask(__name__)

# 🔥 Swagger config + Bearer token support
swagger = Swagger(app, template={
    "swagger": "2.0",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter: Bearer <your_token>"
        }
    }
})


# 🔹 Register Blueprints
app.register_blueprint(generate_bp, url_prefix="/pdf-a3")
app.register_blueprint(extract_bp, url_prefix="/pdf-a3")

# Home route (test)
@app.route('/')
def home():
    return {"message": "PDF-A3 API is running"}

if __name__ == "__main__":
    app.run(debug=True)

