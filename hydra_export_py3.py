#!/usr/bin/python3
import time
import getpass
import json
import requests
import argparse
from warnings import filterwarnings
from colorama import Fore, Style

filterwarnings('ignore')

proxy = "http://127.0.0.1:8080"
proxies = {'http':proxy, 'https':proxy}

s = requests.Session()

SYNACK_API_URL = "https://platform.synack.com/api"
REGISTERED_TARGETS = "/targets/registered_summary"
HYDRA_TARGET = "/hydra_search/search"

def get_args():
	p = argparse.ArgumentParser(description="Hydra API Script")
	p.add_argument('-t','--token',type=str,help="API Token", required=False)
	p.add_argument('-c','--codename',type=str,help="Codename Listing UID", required=False)

	args = p.parse_args()

	return args

def get_uid(access_token, codename):
	headers = {
		'Authorization':f'Bearer {access_token}'
	}
	url = f'{SYNACK_API_URL}{REGISTERED_TARGETS}'
#	data = s.get(url, headers=headers, verify=False, proxies=proxies).json()
	data = s.get(url, headers=headers, verify=False).json()

	for item in data:
		if item['codename'] == codename:
			return item['id']
		else:
			continue

def make_request(url, headers):
	status_code = ""
	try:
#		r = requests.get(url, headers=headers, verify=False, proxies=proxies)
		r = requests.get(url, headers=headers, verify=False)
		if r.status_code == 200:
			print (Fore.YELLOW+"[*] Status Code: " + Style.RESET_ALL + "%s" % r.status_code)
			return r.json()
		else:
			print (Fore.YELLOW+"[*] Status Code: " + Style.RESET_ALL + "%s" % r.status_code)
			return None
	except Exception as e:
		print (Fore.RED+"[!] Error Connecting: "+Style.RESET_ALL + "%s" % str(e))
		return None

def check_errors(data):
	try:
		if data['error']:
			print (Fore.RED+"[!] ElasticSearch Error"+ Style.RESET_ALL)
			return False
	except Exception as e:
		return True

def query_api(access_token, target_codename):

	headers = {"Authorization": "Bearer " + access_token}

	iterator = 1
	next_page = True
	results = []
	results_final = []

	while next_page:
		print (Fore.MAGENTA+"[*] Page %s starting." % str(iterator) + Style.RESET_ALL)
#		try:
		url = f'{SYNACK_API_URL}{HYDRA_TARGET}?page={str(iterator)}&listing_uids={target_codename}&q=%2Bport_is_open%3Atrue'
		target_response = make_request(url, headers)
		if target_response is not None:
			if check_errors(target_response):
				for target in target_response:
					for port in  target['ports']:
						results.append(f"{target['ip']}:{port}")
				print(Fore.CYAN+"Page "+str(iterator)+" done." + Style.RESET_ALL)
				if len(target_response) < 10:
					print(Fore.BLUE+Style.BRIGHT+"Done loading target."+Style.RESET_ALL)
					next_page = False
				iterator += 1
		else:
			print (Fore.YELLOW+"[!] Invalid Response Code. Saving current data and moving on."+Style.RESET_ALL)
			iterator += 1
#		except Exception as e:
#			print (e)
#			next_page = False


	for target in results:
		print (target)

	with open('open-ports.txt', 'w') as f:
		for target in results:
			f.write(target+"\n")

	print (Fore.GREEN+"[+] Open Ports stored in 'open-ports.txt'"+Style.RESET_ALL)

def main():
	args = get_args()

	Listing_UID = get_uid(args.token, args.codename.upper())
	print (Fore.GREEN+"[+] Listing_UID for %s: " % args.codename + Style.RESET_ALL + "%s" % Listing_UID)
	query_api(args.token, Listing_UID)

if __name__ == '__main__':
	main()
