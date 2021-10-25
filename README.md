# Synack Platform API Scripts
Custom created scripts for a better/faster experience at Synack Bug Bounty Platform. 

***Scripts:***
- Hydra open ports export: `hydra_export.py` (Use `hydra_export_py3.py` if you are using python3)
- Download all in-scope IP's for host targets: `scope_download.py`
- Register for all targets at once: `register_all_targets.py`

***Usages:***
- Do not forgot to supply authorization headers for your user and target codename you want to process correctly while asked from command line.
- Auth headers can be easily gathered from the web browser console with the command: `sessionStorage.getItem('shared-session-com.synack.accessToken');` while logged in. 
- Target codenames can also be easily gathered from URL, after clicking the target as: `https://platform.synack.com/targets/<target-codename>/scope`
- For `register_all_targets.py` script, make sure that edit `passed_assessments` array within your own passed assessments from platform.

***Credits:***
- Thanks [Rezn0k](https://twitter.com/Rezn0k) for his contributions on Hydra export script!
