
import paramiko
import os


def remote():
  hostname=os.environ.get("r_hostname")
  username=os.environ.get("r_username")
  password=os.environ.get("r_password")
  
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


'''
if __name__=="__main__":
    a.credentials(r"cred.json")
    remote()'''

          
