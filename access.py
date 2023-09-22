import json
import requests
import hvac

# Initialize the Vault client
vault_url = "http://127.0.0.1:8200"  # Update with your Vault server URL
client = hvac.Client(url=vault_url)

# Authenticate to Vault using a token or your preferred method
vault_token = "hvs.twv58uQtJR68sbuvyQ4R5I4a"  # Update with your Vault token
client.token = vault_token

hostname_ = ""
username_ = ""
password_ = ""


def get_response(token_endpoint, api_endpoint, t_headers, t_params, data):
    global hostname_, username_, password_

    token_response = requests.get(token_endpoint, data=t_params, headers=t_headers)

    token = token_response.json()['access_token']

    authen = f"Bearer {token}"

    header = {"Content-Type": "application/json", "Authorization": authen}

    response = requests.post(api_endpoint, headers=header, data=json.dumps(data))
    result = response.json()['Result']
    hostname_ = result[0]["ServerIp"]
    username_ = result[0]["UserName"]
    password_ = result[0]["Password"]
    print("Success retrieved")


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
        raise Exception(f"The file {file} does not exist.")


def call_api(ip, service_type, user, DBname, time):
    token_endpoint = base_url + "/arconToken"
    api_endpoint = base_url + "/api/ServicePassword/GetTargetDevicePasskey"

    t_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    t_params = cred.copy()
    if 'base' in t_params:
        del t_params['base']

    body_content = [
        {
            "ServerIp": "15.185.66.219",
            "ServiceTypeID": "7",
            "UserName": "L1admin",
            "DbInstanceName": "",
            "OpenForHours": "1"
        }]

    val = {"ServerIp": ip, "ServiceTypeID": service_type, "UserName": user, "DbInstanceName": DBname,
           "OpenforHours": time}

    body_content.append(val)
    
    # Retrieve data from the API
    get_response(token_endpoint, api_endpoint, t_headers, t_params, body_content)
    
    # Store the retrieved credentials in Vault
    store_credentials_in_vault()


def store_credentials_in_vault():
    global hostname_, username_, password_
    
    # Define the path in Vault where you want to store the data
    secret_path = "secret/mysecrets/mykey"  # Update with your desired path
    
    # Create a dictionary to store the credentials
    data = {
        "hostname": hostname_,
        "username": username_,
        "password": password_
    }
    
    try:
        client.secrets.kv.v2.create_or_update_secret(
            path=secret_path,
            secret=data
        )
        print("Data stored successfully in Vault.")
    except hvac.exceptions.Forbidden as e:
        print("Failed to store data in Vault. Forbidden: Permission denied.")
    except Exception as e:
        print("Failed to store data in Vault:", str(e))



    
if __name__ == "__main__":
    credentials(r"cred.json")
    call_api("15.185.66.219", "7", "L1admin", "", "1")
