import access as a 
import machine_access as m

a.credentials(r"cred.json")


a.call_api("15.185.66.219", "7", "L1admin", "", "1")


m.remote()