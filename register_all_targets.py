import json
import requests
import warnings

requests.adapters.DEFAULT_RETRIES = 10
warnings.filterwarnings("ignore")
auth_header = raw_input("Please enter your Synack Auth Header (Command from web console: sessionStorage.getItem('shared-session-com.synack.accessToken')): ")
headers = {"Authorization": "Bearer "+auth_header}

iter = 1
next_page = True
slugs = []
passed_assessments = ["Web Application", "Host", "Mobile", "Hardware", "Reverse Engineering", "Source Code"]

print "Getting target slugs."
while next_page:
    url = "https://platform.synack.com/api/targets?filter%5Bprimary%5D=unregistered&filter%5Bsecondary%5D=all&filter%5Bcategory%5D=all&sorting%5Bfield%5D=dateUpdated&sorting%5Bdirection%5D=desc&pagination%5Bpage%5D="+str(iter)
    target_response = requests.get(url, headers=headers, verify=False).json()
    if (len(target_response)!=0):
        for i in range (len(target_response)): 
            if target_response[i]["category"]["name"] in passed_assessments:
                slugs.append(str(target_response[i]["slug"]))
        iter += 1
        print "Page "+str(iter)+" done."
    else:
        next_page = False
print "All slugs for not-registered targets are successfully gathered!"
print "Total count of not-registered targets are: "+str(len(slugs))
print "Starting process of registering all targets."
for i in range (len(slugs)): 
    url = "https://platform.synack.com/api/targets/"+slugs[i]+"/signup"
    target_response = requests.post(url, headers=headers, verify=False, json={"ResearcherListing":{"terms":1}})
    if target_response.status_code == 200:
        print "Registered target with slug "+slugs[i]+" successfully!"
    else:
        print "Error while registering target with slug "+slugs[i]
print "All processes are completed."
