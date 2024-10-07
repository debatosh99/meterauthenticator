import os
import psycopg2
import requests
import json
import logging
# from flask import Flask, abort, jsonify, _request_ctx_stack, request, Response
from flask import Flask, abort, jsonify, request, Response
from dotenv import load_dotenv
from functools import wraps
# from jose import jwt
from jwt import PyJWKClient
import jwt

load_dotenv()

DATABASE = os.getenv('database')
USER = os.getenv('user')
PASSWORD = os.getenv('password')
HOST = os.getenv('host')
PORT = os.getenv('port')


API_AUDIENCE = os.getenv('api_audience')
ALGORITHMS = os.getenv('algorithms')
JWK_URL = os.getenv('jwk_url')
AUTH_ISSUER = os.getenv('auth_issuer')

app = Flask(__name__)

log_format = "%(asctime)s::%(levelname)s::%(name)s::" \
             "%(filename)s::%(lineno)d::%(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)

# myconn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
# mycursor = myconn.cursor()


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    try:
        parts = auth.split()
        token = parts[1]  # parts[0] will be 'bearer' & parts[1] the actual token
        return token
    except:
        return Response("No access token found", status=401)


def requires_auth(f):
    """Determines if the Access Token is valid
    """

    @wraps(f)
    def decorated(*args, **kwargs):

        # Get token from the authorization header
        token = get_token_auth_header()
        app.logger.info('Token is: %s', token)

        # Get Public Key for the Authorization Server for the Key ID listed in the token header
        # url = "http://localhost:8080/realms/myorg/protocol/openid-connect/certs"
        url = JWK_URL
        response = requests.get(url)
        jwks = json.loads(response.content)
        unverified_header = jwt.get_unverified_header(token)

        jwks_client = PyJWKClient(url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

        # Use the Public Key to decode the jwt
        try:
            payload = jwt.decode(
                token,
                # rsa_key,
                signing_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                # issuer="http://localhost:8080/realms/myorg/"
                issuer=AUTH_ISSUER,
                options={"verify_signature": True, "verify_exp": True, "verify_iss": True, "verify_aud": False}
            )
        # In case of issues with the the token
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
            return Response("The access token provided has expired", status=401)
        except jwt.ExpiredSignatureError:
            print("Expired signature.")
            return Response("The access token provided has expired signature", status=401)
        except jwt.InvalidIssuerError:
            print("Invalid issuer.")
            return Response("The access token provided has invalid issuer", status=401)
        except jwt.InvalidAudienceError:
            print("Invalid audience.")
            return Response("The access token provided has invalid audience", status=401)
        except jwt.InvalidTokenError:
            print("Invalid token.")
            return Response("The access token provided has issues", status=401)
        except:
            return Response("The access token provided has issues", status=401)
        # _request_ctx_stack.top.current_user = payload
        return f(*args, **kwargs)

    return decorated


@app.route("/")
def home():
    return 'Hello World'


@app.route("/api/1.0/products")
# @cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def products_view():
    # try:
    #     global mycursor
    #     mycursor.execute("SELECT * FROM core.dim_product")
    #     db = []
    #     for x in mycursor:
    #         db.append(x)
    #     return jsonify(db)
    try:
        myjson = {"Greet":"Hello"}
        return jsonify(myjson)
    except IndexError:
        abort(404)


# @app.route("/api/1.0/products/<id>")
# def product_view(id):
#     try:
#         global mycursor
#         cmd = "SELECT * FROM core.dim_product where product_id = " + "'" + id + "'"
#         mycursor.execute(cmd)
#         db = []
#         for x in mycursor:
#             db.append(x)
#         return jsonify(db)
#     except IndexError:
#         abort(404)


if __name__ == '__main__':
    app.run(debug=False, port=5000)