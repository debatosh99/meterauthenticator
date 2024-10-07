###  function to obtain a new OAuth 2.0 token from the authentication server and use this token to make api call
import sys
import requests
import json
import logging
import time

logging.captureWarnings(True)

def get_new_token():
    auth_server_url = "http://localhost:8080/realms/myorg/protocol/openid-connect/token"
    client_id = 'mywebapp'
    client_secret = 'kpUdB9LnM5DNUUlqT0nIy2WGN7HcS5TG'
    token_req_payload = {'grant_type': 'client_credentials'}

    token_response = requests.post(auth_server_url,
                               data=token_req_payload, verify=False, allow_redirects=False,
                               auth=(client_id, client_secret))

    if token_response.status_code != 200:
        print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
        sys.exit(1)
    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']


token = get_new_token()
print("The access token is :{}".format(token))


# test_api_url = "https://apigw-pod1.dm-us.informaticacloud.com/t/apim.usw1.com/get_employee_details"
# while True:
#     api_call_headers = {'Authorization': 'Bearer ' + token}
#     api_call_response = requests.get(test_api_url, headers=api_call_headers, verify + False)
#     if api_call_response.status_code == 401:
#         token = get_new_token()
#     else:
#         print(api_call_response.text)
#
# time.sleep(30)