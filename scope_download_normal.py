import requests
import warnings
import json
import os

warnings.filterwarnings("ignore")

token = raw_input("Please enter your Synack Auth Header (Command from web console: sessionStorage.getItem('shared-session-com.synack.accessToken')): ")
target_code = raw_input("Please enter your target codename: ")

blocks = []
x = 1

print ("Downloading scope for target.")
response = requests.get('https://platform.synack.com/api/targets/'+target_code+'/cidrs',params={'page': x},headers={'Authorization': 'Bearer '+token},verify=False)
temp = json.dumps(response.json()['cidrs']).replace("[","").replace("]","").replace("\"","").replace(", ","\n").split("\n")
blocks.extend(temp)
print("Page "+str(x)+" done.")
while len(temp) > 1:
    x = x + 3
    response = requests.get('https://platform.synack.com/api/targets/'+target_code+'/cidrs',params={'page': x},headers={'Authorization': 'Bearer '+token},verify=False)
    temp = json.dumps(response.json()['cidrs']).replace("[","").replace("]","").replace("\"","").replace(", ","\n").split("\n")
    blocks.extend(temp)
    print("Page "+str(x)+" done.")
blocks = list(set(blocks))
if os.path.isfile("blocks.txt"):
	os.remove("blocks.txt")
f = open("blocks.txt","w+")
for i in range (len(blocks)):
	if blocks[i] != "": f.write(blocks[i]+"\n")
f.close()
print ("All done! Blocks have been added to blocks.txt file.")