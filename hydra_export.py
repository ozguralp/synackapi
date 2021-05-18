import json
import requests

requests.adapters.DEFAULT_RETRIES = 10
SYNACK_API_URL = "https://platform.synack.com/api"
REGISTERED_TARGETS = "/targets/registered_summary"
ALL_TARGETS = "/targets/"
HYDRA_TARGET = "/hydra_search/search"

auth_header = raw_input("Please enter your Synack Auth Header (Command from web console: sessionStorage.getItem('shared-session-com.synack.accessToken')): ")
target_codename = raw_input("Please enter your target codename: ")
headers = {"Authorization": "Bearer "+auth_header}

iterator = 1
next_page = True
results = [[],[]]
results_final = []

while next_page:
    try:
        url = SYNACK_API_URL + HYDRA_TARGET + "?page="+str(iterator)+"&listing_uids="+target_codename+"&q=%2Bport_is_open%3Atrue"
        target_response = requests.get(url, headers=headers).json()
        for i in range (len(target_response)): 
            ports = str(target_response[i]["ports"]).split("}}}}")
            for j in range (len(ports)-1):
                results[0].append((target_response[i]["ip"]))
                results[1].append(str(ports[j]).split("'")[1])
        print("Page "+str(iterator)+" done.")
        if len(target_response) < 10:
            print("Done loading target.")
            next_page = False
        iterator += 1
    except Exception as e:
        print(e)
        next_page = False

for i in range (len(results[0])): 
    results_final.append (str(results[0][i])+":"+str(results[1][i]))
results_final.sort()

for i in range (len(results_final)): 
    print results_final[i]
