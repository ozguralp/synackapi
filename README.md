# Synack Platform API Scripts
Custom created scripts for a better/faster experience at Synack Bug Bounty Platform. 

***Scripts:***
- Hydra open ports export: `hydra_export.py`
- Download all in-scope IP's for host targets: `scope_download_normal.py`
- Download all in-scope IP's for host targets (Threaded mode): `scope_download_threaded.py`

***Usages:***
- Do not forgot to supply authorization headers for your user and target codename you want to process correctly while asked from command line.
- Auth headers can be easily gathered from the web browser console with the command: `sessionStorage.getItem('shared-session-com.synack.accessToken');` while logged in. 
- hydra_exports.py works both with python3 and python2 to use it simply $ python3 hydra_exports.py --key=<long stringhere> --codename=<codename of the target> the output will be displayed as well as saved in a file. 
- Target codenames can also be easily gathered from URL, after clicking the target as: `https://platform.synack.com/targets/<target-codename>/scope`
- For `scope_download_threaded.py` script, `max_page_count` should be increased if the target scope is too big. It can also be confirmed with the curl command: `curl -i -s -k  -X $'GET' -H $'Host: platform.synack.com' -H $'Authorization: Bearer <auth-token>' $'https://platform.synack.com/api/targets/<target-code>/cidrs?page=<max-page-count>'`. If it returns empty body while connected to the LP, then it can be said that the script covers all scope. No other configuration is needed for non-threaded `scope_download_normal.py` script.

***Credits:***
- Thanks [Rezn0k](https://twitter.com/Rezn0k) for his contributions on Hydra export script!
