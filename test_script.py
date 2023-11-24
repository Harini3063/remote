import remote_access_sdk as a 


a.credentials(r"cred.json")


a.call_api("15.185.66.219", "7", "L1admin", "", "1")


a.remote()
