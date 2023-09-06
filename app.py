import json
import requests
hostname_=""
username_=""
password_=""


def get_response(api_endpoint, header, data):
    response = requests.post(api_endpoint, headers=header, data=json.dumps(data))  
    result = response.json()['Result']
    hostname_=result[0]["ServerIp"]
    username_=result[0]["UserName"]
    password_=result[0]["Password"]
    #print(hostname_,username_,password_)
    return hostname_,username_,password_

def call_token():
    token_URL = "https://pimapi.arconnet.com:7443/arconToken"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    credentials = {
        "username": "bXlsb2dpbjE=",
        "password": "bXlsb2dpbkA=",
        "grant_type": "password"
    }
    response = requests.post(token_URL, data=credentials, headers=headers)
    tok = response.json().get('access_token')  # Use .get() to handle missing keys
    return tok

def call_api(ip, service_type, user, DBname, time):
    token = call_token()
    base = "https://pimapi.arconnet.com:7443"
    api_endpoint = base + "/api/ServicePassword/GetTargetDevicePasskey"
    authen = f"Bearer {token}"  # 'Bearer' should be capitalized
    header = {"Content-Type": "application/json", "Authorization": authen}
    
    # Define the body content as a list of dictionaries
    body_content =[ 
        {
            "ServerIp": "15.185.66.219",
            "ServiceTypeID": "7",
            "UserName": "L1admin",
            "DbInstanceName": "",
            "OpenForHours": "1"
        }]
        
    

    val = {"ServerIp": ip, "ServiceTypeID": service_type, "UserName": user, "DbInstanceName": DBname, "OpenforHours": time}
    
    # Add 'val' to the body content
    body_content.append(val)
    
    return get_response(api_endpoint, header, body_content)
