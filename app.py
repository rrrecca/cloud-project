from flask import Flask, jsonify
from auth import auth_required

app = Flask(__name__)


@app.route("/test", methods=["GET"])
@auth_required
def test_route():
    return jsonify({"message": "token is valid"}), 200


if __name__ == "__main__":
    app.run(debug=True)
