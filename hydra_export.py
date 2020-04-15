import argparse
import sys
import json
import requests

SYNACK_API_URL = "https://platform.synack.com/api"
REGISTERED_TARGETS = "/targets/registered_summary"
ALL_TARGETS = "/targets/"
HYDRA_TARGET = "/hydra_search/search"

## Documentation

parser = argparse.ArgumentParser(description="Synack Hydra host scope download")
parser.add_argument('--key', type=str, metavar='', required=True, help="Please enter your Synack Auth Header. Use this command in web browser console : sessionStorage.getItem('shared-session-com.synack.accessToken')")
parser.add_argument('--codename', type=str, metavar='', required=True, help="Please enter your target codename. It should be in the URL https://platform.synack.com/targets/<Codename>")
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args= parser.parse_args()


auth_header = args.key
target_codename = args.codename
headers = {"Authorization": "Bearer "+auth_header}

iterator = 1
next_page = True
results = [[],[]]
results_final = []

## Get the json blob

while next_page:
    try:
        url = SYNACK_API_URL + HYDRA_TARGET + "?page="+str(iterator)+"&listing_uids="+target_codename+"&q=%2Bport_is_open%3Atrue"
        target_response = requests.get(url, headers=headers).json()
        print("[+] Page "+str(iterator))
        for blobs in target_response:
            ipAddress= str(blobs['ip'])
            portNum= str(blobs['ports']).split("'")[1]
            print(ipAddress+":"+str(blobs['ports']).split("'")[1])
            results_final.append(ipAddress+":"+portNum)
        if len(target_response) < 10:
            print("Done loading target.")
            next_page = False
        iterator += 1
    except Exception as e:
        print(e)
        next_page = False


## To save the final results

results_final.sort()
FileName= "hydraHost_"+str(target_codename)+".txt"
f = open(FileName,"w+")

for entry in range(len(results_final)):
    f.write(str(results_final[entry])+"\n")

f.close()