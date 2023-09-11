
import paramiko
import app as a 

def remote():
  hostname,username,password=a.call_api("15.185.66.219", "7", "L1admin", "", "1")
  
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

          
