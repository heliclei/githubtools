import requests
import sys
url = 'https://api.github.com/repos/HelloJenkins/cocos2d-x/hooks'
token = {'access_token':''}
token['access_token']=sys.argv[1]
r = requests.get(url,params=token)
print r.json()

