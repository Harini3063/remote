import paramiko
import os
import hvac

# Function to retrieve data from Vault
def retrieve_credentials_from_vault():
    # Initialize the Vault client
    vault_url = "http://127.0.0.1:8200"  # Update with your Vault server URL
    client = hvac.Client(url=vault_url)

    # Authenticate to Vault using a token or your preferred method
    vault_token = "hvs.twv58uQtJR68sbuvyQ4R5I4a"  # Update with your Vault token
    client.token = vault_token

    # Define the path from which you want to retrieve credentials
    secret_path = "secret/mysecrets/mykey"  # Update with your desired path

    try:
        response = client.secrets.kv.v2.read_secret_version(
            path=secret_path
        )
        credentials = response["data"]["data"]
        return credentials
    except hvac.exceptions.Forbidden as e:
        print("Failed to retrieve credentials from Vault. Forbidden: Permission denied.")
    except Exception as e:
        print("Failed to retrieve credentials from Vault:", str(e))
    return None


def remote():
    # Retrieve credentials from Vault
    credentials = retrieve_credentials_from_vault()
    if credentials is None:
        exit()

    # Extract credentials
    hostname = credentials.get("hostname")
    username = credentials.get("username")
    password = credentials.get("password")
    print(hostname,username,password)
    commands = [
        "pwd",
        "id",
        "uname",
        "date",
        "hostname -i",
        "whoami",
        "ls"
    ]

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=hostname, username=username, password=password)
        print("Connected to the machine!!!")

    except Exception as e:
        print("Error!!! Cannot connect to Server:", str(e))
        exit()

    for c in commands:
        print("=" * 30, c, "=" * 30)
        stdin, stdout, stderr = client.exec_command(c)
        print(stdout.read().decode())
        error = stderr.read().decode()
        if error:
            print(error)

