import requests
import sys
import json
url = 'https://api.github.com/repos/HelloJenkins/cocos2d-x/hooks/'+sys.argv[1]

token = {'access_token':"1ec353bd8bab5a661446a656cf144fb0e468fe18"}
payload =  {"config": {"url": "http://115.28.134.83:8000/job/HelloJenkins-Trigger/buildWithParameters?token=331c4f4de07dc0b4c6fe9cd5e626cb3ec0caba01","content_type": "form","insecure_ssl": "1"}}

r = requests.patch(url, params=token, data=json.dumps(payload))
print r.json()

