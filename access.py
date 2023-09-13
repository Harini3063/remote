import json
import requests
import paramiko

hostname_=""
username_=""
password_=""


#funtion to get token and and retrieves the hostname,username,password
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
    print("success retrieved")

   
#function to read the credentials
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



#makes an api call 
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


#function to connect to remote machine and run commands
def remote():
  hostname=hostname_
  username=username_
  password=password_
  
  commands = [
      "pwd",
      "id",
      "uname",
      "date",
      "hostname -i",
      "whoami",
      "ls" 
  ]


  client=paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


  try:
      client.connect(hostname=hostname,username=username,password=password)
      print("Connected to the machine!!!")
  except:
      print("Error!!! Cannot connect to Server")
      exit()  



  for c in commands:
      print("="*30,c,"="*30)
      stdin,stdout,stderr=client.exec_command(c)
      print(stdout.read().decode())    
      error=stderr.read().decode()
      if error:
          print(error)