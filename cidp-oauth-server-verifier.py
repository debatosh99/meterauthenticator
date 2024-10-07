import jwt


def authenticate_jwt(access_token, secret_key):
  """
  Authenticates a JWT access token using a secret key.

  Args:
      access_token (str): The JWT access token to authenticate.
      secret_key (str): The secret key used to sign the JWT.

  Returns:
      bool: True if the token is valid, False otherwise.
  """

  try:
    decoded_token = jwt.decode(access_token, secret_key, algorithms=["RS256"], options={"verify_signature": True, "verify_exp": True, "verify_iss": False, "verify_aud": False})
    return True
  except jwt.ExpiredSignatureError:
    print("Token has expired.")
    return False
  except jwt.ExpiredSignatureError:
    print("Expired signature.")
    return False
  except jwt.InvalidIssuerError:
    print("Invalid issuer.")
    return False
  except jwt.InvalidAudienceError:
    print("Invalid audience.")
    return False
  except jwt.InvalidTokenError:
    print("Invalid token.")
    return False
  except jwt.InvalidKeyError:
    print("Invalid key")
    return False

# Example usage
access_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJpRGhNeThfZmd6NXFtbnRNb1pITmNTbHZYNmpPa05xbFp4M0F3UDR6ME1RIn0.eyJleHAiOjE3MjgyMTE5MzgsImlhdCI6MTcyODIxMDEzOCwianRpIjoiOTU3YzE4NGEtY2JkYy00MmQ5LTkxYjEtNjgxZTQwZTJlZDAxIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9teW9yZyIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiI5NzhlZGQ1Ni1lY2QxLTQ0NWMtOGJlNi1jMGFhMTkwM2UwNTkiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJteXdlYmFwcCIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cDovL2xvY2FsaG9zdDozMDAwIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsImRlZmF1bHQtcm9sZXMtbXlvcmciLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7Im15d2ViYXBwIjp7InJvbGVzIjpbInVtYV9wcm90ZWN0aW9uIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImNsaWVudEhvc3QiOiIwOjA6MDowOjA6MDowOjEiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzZXJ2aWNlLWFjY291bnQtbXl3ZWJhcHAiLCJjbGllbnRBZGRyZXNzIjoiMDowOjA6MDowOjA6MDoxIiwiY2xpZW50X2lkIjoibXl3ZWJhcHAifQ.C1oQf_nvKliQOmOgCAzTIltwuefjf8vurwnIy188jxAsfclMExE67ASsW-Aa7iB5EEmgTAYiqWMwivD4r-rn4ir9_r6s5gdF5pj20IlvhXbY_Q0VRh1CC2RzsdfhKiouKPNGnD0swwECFxVF7_6GltvLPMLJ7pyM6DpA8Lwg9WCZ6jXr_a-TcQsF434fubT_EQblqULTBpER78ezDBEUsVl7seWXjSCZ9STUIdyNDQhONb3NxCPxh59gQ2B20GyjS0MgCL_ETzCannBQKf5i4KuSgKMGgjlpvCXKgXGq84q2W7Fvks1gHFhuwEYmQQAf34ISBeeKZYMzJTiTpFm5Fw"
#secret_key = "kpUdB9LnM5DNUUlqT0nIy2WGN7HcS5TG"

secret_key = "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsyCoX3BTJwXDRBoxd3wcochRmhbXsEoWL5oIL37gxIxja5r0McOOAKB1e2ZDVAA0l77Opz8E+b4nQYHwnYtoYNO0aTOwf8FV++QsS293nVRfiYIR8SuS1mcmD6AjBJEb4rW07QGvSMnywaP/Huk05Et0Hi8eJte1aRgp+HPCiXdfT5j3htEcYLYH527il8oKf6PdFIt3yX5hszq47N/2+sTOSNwdFyLpfxUoMr7aBOEq+ZC3tmTM8lEE04gS9TwvkUkmoxXZiT1x7lZTVi6ODO2JM1DVL3prtrNeq8VNrTnByYthVY0QQ3Z7tGHzsuGAy+u5ZFs/WRzr3mCWDo7bUwIDAQAB-----END PUBLIC KEY-----"

if authenticate_jwt(access_token, secret_key):
  print("Token is valid.")
else:
  print("Token is invalid.")