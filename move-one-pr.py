import re
import json
import requests
import traceback
import sys

tk = 'a135a2fbce040b1988225f1c72d021fe5b90d07e'
token = {'access_token':tk}

http_proxy = 'http://127.0.0.1:8087'
proxyDict = {'http':http_proxy,'https':http_proxy}

target_repo = 'https://api.github.com/repos/cocos2d/cocos2d-x/'
src_repo = 'https://api.github.com/repos/cocos2d/cocos2d-x/'
target_branch = 'v3'
src_branch = 'develop'

def create_pull_request(head, base, body, title):
	pr = {}
	pr['title'] = '[ci skip]'+title
	pr['body'] = body
	pr['head'] = head
	pr['base'] = base
	print pr
	return pr

def send_pull_reqeust(repo, pr):
	Headers = {"Authorization":"token " + tk} 
	try:
		r = requests.post(repo + 'pulls', data = json.dumps(pr), headers = Headers, proxies = proxyDict)
		#print r.status
	except:
		traceback.print_exc()



def get_one_pr(repo_url, pr):
	r = requests.get(repo_url+'pulls/'+str(pr), params = token, proxies = proxyDict)
	l = r.json()
	print l
 	return l


pr_num = sys.argv[1]

srcPr = get_one_pr(src_repo, pr_num)

composedPR = create_pull_request(srcPr['head']['label'], target_branch, srcPr['body'], srcPr['title'])

send_pull_reqeust(target_repo, composedPR)


