from flask import Flask
from flasgger import Swagger
from routes.generate import generate_bp
from routes.extract import extract_bp

app = Flask(__name__)


app.register_blueprint(generate_bp)
app.register_blueprint(extract_bp)
# Initialize Swagger
swagger = Swagger(app)

# Home route (test)
@app.route('/')
def home():
    return {"message": "PDF-A3 API is running"}

# Run the app
if __name__ == '__main__':
    app.run(debug=True)