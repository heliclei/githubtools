import requests
import traceback
import json

statuses_url = 'https://api.github.com/repos/heliclei/cocos2d-x/statuses/70d8c2a7b5932102348395e66f6fdf0903c8e375'
data = {"state":"pending", "target_url":"http://115.28.134.83/", "context":"IOS", "description":"start build IOS"}
access_token = '6fba5b9dea2fc024fa4d594eca32e0982777722a'
Headers = {"Authorization":"token " + access_token} 

try:
    requests.post(statuses_url, data=json.dumps(data), headers=Headers)
except:
    traceback.print_exc()