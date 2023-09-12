import json
import requests
import os



hostname_=""
username_=""
password_=""



def get_response(token_endpoint,api_endpoint, t_headers,t_params,data):
    global hostname_, username_, password_
    
    token_response = requests.get(token_endpoint, data=t_params, headers=t_headers)
    
    token = token_response.json()['access_token']
    
    authen = f"Bearer {token}"
    
    header = {"Content-Type": "application/json", "Authorization": authen}
    
    
    response = requests.post(api_endpoint, headers=header, data=json.dumps(data))  
    result = response.json()['Result']
    hostname_=result[0]["ServerIp"]
    username_=result[0]["UserName"]
    password_=result[0]["Password"]
    Environ_var()

def Environ_var():
    global hostname_, username_, password_
    # Replace with your CircleCI API token and project name
    circleci_token = 'CCIPAT_MNBTb4Ygh59mAPSkpaxbQh_4d89f81c862fbf1853dd95fad43e06315b394c0f'
    project_slug = 'Harini3063/remote'

    # Define the URL for setting an environment variable
    url = f'https://circleci.com/api/v2/project/{project_slug}/envvar'

    # Define the environment variable to set
  
    variables = {
    'host': hostname_,
    'user': username_,
    'passkey': password_
    }

    # Define the request headers with your API token
    headers = {
        'Circle-Token': circleci_token,
        'Content-Type': 'application/json'
    }

    # Loop through the dictionary and set each environment variable
    for name, value in variables.items():
        payload = {
            'name': name,
            'value':value
        }
    
    # Make the POST request to set the environment variable
    response = requests.post(url, json=payload, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 201:
        print(f"Environment variable '{variable_name}' set successfully.")
    else:
        print(f"Failed to set environment variable '{variable_name}'. Status code: {response.status_code}")
        print(response.text)

    # Define the request headers with your API token

        

def credentials(file):
    try:
        with open(file) as f:
            global cred
            cred = json.load(f)
        
        if cred.keys() >= {'base', 'username', 'password', 'grant_type'}:
            global base_url
            base_url = cred.get('base')
            print("The file is read")
        else:
            raise Exception("Valid Keys are not present")
    except FileNotFoundError:
        raise Exception(f"The file '{file}' does not exist.")
    except json.JSONDecodeError as e:
        raise Exception(f"Error decoding JSON: {str(e)}")




def call_api(ip, service_type, user, DBname, time):
    
    token_endpoint=base_url + "/arconToken"
    api_endpoint = base_url + "/api/ServicePassword/GetTargetDevicePasskey"
      
    t_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
   
    t_params=cred.copy()
    if 'base' in t_params:
        del t_params['base']
    
    body_content =[ 
        {
            "ServerIp": "15.185.66.219",
            "ServiceTypeID": "7",
            "UserName": "L1admin",
            "DbInstanceName": "",
            "OpenForHours": "1"
        }]

    val = {"ServerIp": ip, "ServiceTypeID": service_type, "UserName": user, "DbInstanceName": DBname, "OpenforHours": time}
    
    
    body_content.append(val)
    
    
    
    return get_response(token_endpoint,api_endpoint, t_headers,t_params,body_content)

