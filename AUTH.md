# auth.py — How to use

## What's in here

- `validate_token(token)` — checks if a JWT token is valid
- `auth_required` — decorator that protects a route

---

## Protecting a route

Import and add `@auth_required` above any route you want to protect:

```python
from auth import auth_required

@blueprint.route("/generate", methods=["POST"])
@auth_required
def generate():
    # only runs if the token is valid
```

That's it. The decorator handles everything — no extra code needed inside the function.

---

## What the decorator checks

1. Is the `Authorization` header present? If not → `401`
2. Is the token valid and not expired? If not → `403`
3. Does the token have a `sub` claim? If not → `403`
4. All good → your function runs

---

## Expected header format

```
Authorization: Bearer <your-jwt-token>
```

---

## Responses when auth fails

```json
// 401 — no token sent
{ "error": "No token provided" }

// 403 — token invalid or expired
{ "error": "Invalid or expired token" }
```

---

## How validate_token works internally

```python
validate_token("Bearer eyJhbGci...")
```

1. Strips `"Bearer "` prefix
2. Fetches Frontegg's public key using the `kid` from the token header
3. Verifies the RS256 signature and expiry
4. Returns `True` if valid, `False` on any error

---

## JWKS URL

The public key is fetched from this Frontegg endpoint (configured at the top of `auth.py`):

```
https://app-4erd7c2ivzcz.frontegg.com/.well-known/jwks.json
```

To use a different Frontegg app, update `JWKS_URL` in `auth.py`.

---

## Running the server

```bash
source venv/bin/activate
python app.py
```

`app.py` is a minimal Flask server with one test route:

```python
@app.route("/test", methods=["GET"])
@auth_required
def test_route():
    return jsonify({"message": "token is valid"}), 200
```

Test it:

```bash
# without token → 401
curl -X GET http://127.0.0.1:5000/test

# with token → 200
curl -X GET http://127.0.0.1:5000/test \
  -H "Authorization: Bearer <your-jwt-token>"
```
