README 


1)remote_access_sdk is the main script.It has functions such as

	-read_credentials - reads the credentials in json format

	-call_api- makes an api call 

	-get_response - its retrieves the json response
	
	-remote - it establishes an SSH connection and enable to run commands on the remote machine 

2)test_script it imports the remote_access_sdk and calls the function to test it

3)config.yml is the configuration file for circle ci to automate the process

4)creds.json contains the input credentials

5)require.txt contains the modules to be imported
