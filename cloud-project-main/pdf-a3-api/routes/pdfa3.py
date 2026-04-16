from flask import Blueprint, request, jsonify
from auth import verify_token

pdfa3_bp = Blueprint("pdfa3", __name__)