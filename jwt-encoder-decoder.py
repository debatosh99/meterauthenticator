import jwt

key = "kpUdB9LnM5DNUUlqT0nIy2WGN7HcS5TG"
encoded = jwt.encode({"name": "tommy"}, key, algorithm="HS256")
print(encoded)

# jwt.decode(encoded, key, algorithms="HS256")
# {'some': 'payload'}

try:
    decoded_token = jwt.decode(encoded, key, algorithms=["HS256"], options={"verify_signature": True, "verify_exp": True, "verify_iss": True, "verify_aud": False})
    print(decoded_token)
except jwt.ExpiredSignatureError:
    print("Token has expired.")
except jwt.ExpiredSignatureError:
    print("Expired signature.")
except jwt.InvalidIssuerError:
    print("Invalid issuer.")
except jwt.InvalidAudienceError:
    print("Invalid audience.")
except jwt.InvalidTokenError:
    print("Invalid token.")