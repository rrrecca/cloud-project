# Library to decode and verify JWT tokens
import jwt

# Library to make HTTP requests
import requests

# Python utility to preserve the original function name when wrapping it with a decorator
import functools

# request → gives access to incoming request data (headers, body, etc.)
# jsonify → converts a Python dict to a JSON response
from flask import request, jsonify

# The URL where Frontegg publishes its public keys (used to verify token signatures)
JWKS_URL = "https://app-4erd7c2ivzcz.frontegg.com/.well-known/jwks.json"

# Create the JWKS client once at startup — it fetches and caches Frontegg's public keys
# Doing this once is more efficient than fetching on every request
jwks_client = jwt.PyJWKClient(JWKS_URL)


def validate_token(token):
    try:
        # Strip the "Bearer " prefix to get the raw JWT string
        token = token.replace("Bearer ", "")

        # Read the kid (key ID) from the token header and find the matching public key
        # kid tells us which of Frontegg's public keys was used to sign this token
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        # Verify and decode the token using Frontegg's public key
        # - signing_key.key → the actual RSA public key to verify the signature
        # - algorithms=["RS256"] → the algorithm Frontegg uses to sign tokens
        # - verify_aud: False → skip the audience check (Frontegg adds an aud claim we don't need to validate)
        # This also automatically checks if the token is expired
        decoded = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False}
        )

        # Check that the sub claim exists — sub is the unique user ID inside the token
        # If it's missing, the token is not a valid user token
        if "sub" not in decoded:
            return False

        # All checks passed — token is valid
        return True

    except Exception as e:
        # Any error (expired token, bad signature, malformed JWT, etc.) lands here
        # Print the error for debugging and return False to reject the request
        print(f"[validate_token error] {e}")
        return False


# Decorator that protects a route by checking the JWT token before the function runs
# Usage: add @auth_required above any route you want to protect
def auth_required(route_fn):
    # Preserves the original route function's name (required by Flask internally)
    @functools.wraps(route_fn)
    def wrapper(*args, **kwargs):
        # Read the Authorization header from the incoming request
        token = request.headers.get("Authorization")

        # If no token was sent at all, reject with 401 Unauthorized
        if not token:
            return jsonify({"error": "No token provided"}), 401

        # If the token is invalid or expired, reject with 403 Forbidden
        if not validate_token(token):
            return jsonify({"error": "Invalid or expired token"}), 403

        # Token is valid — call the actual route function
        return route_fn(*args, **kwargs)

    # Return the wrapper so Flask uses it instead of the original route function
    return wrapper
