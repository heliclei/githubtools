#comment_pr.py

import re
import json
import requests
import traceback

tk = 'a135a2fbce040b1988225f1c72d021fe5b90d07e'
token = {'access_token':tk}

http_proxy = 'http://127.0.0.1:8087'
proxyDict = {'http':http_proxy,'https':http_proxy}

repo_base = 'https://api.github.com/repos/cocos2d/cocos2d-x/'
old_branch = 'develop'
new_branch = 'v3'

def send_comments(old_pr, new_pr_number):
	Headers = {"Authorization":"token " + tk} 
	data = {}
	user = old_pr['user']['login']
	body = "Dear " + user + ":\r\n" + "  We have created a new branch 'v3' to replace branch 'develop', " + \
	"and this PR has been moved from 'develop' branch to 'v3' branch, " + \
	"the new PR is https://github.com/cocos2d/cocos2d-x/pull/"+str(new_pr_number) +"\r\n" + \
	"The old 'develop' branch will be deleted soon, and this PR will be closed accordingly."
	data['body'] = body
	comments_url = old_pr['comments_url']
	try:
		#print data
		print comments_url
		requests.post(comments_url, data = json.dumps(data), headers = Headers, proxies = proxyDict)
	except:
		traceback.print_exc()



def get_all_pr(repo_url, branch):
	url = repo_url + 'pulls?base='+branch
	print url
	r = requests.get(url, params = token, proxies = proxyDict)

	l = r.json()
	#print r.json()
	print len(l)
	p = re.compile("<(\S+)>; rel=\"next\"")
	h = r.headers
	print h

	if('link' not in h):
		return l
	
	result = p.search(h['link'])

	while(result is not None):
		next_url = result.group(1)
 		r = requests.get(next_url, params = token, proxies = proxyDict)
 		#print r.json()
 		l += r.json()
 		h = r.headers
		print h['link']
		result = p.search(h['link'])
 	return l

new_pr_list = get_all_pr(repo_base, new_branch)
r = requests.get(repo_base+'pulls?base='+old_branch, params = token, proxies = proxyDict)
old_pr_list = r.json()
for pr_old in old_pr_list:
	for pr_new in new_pr_list:
		if pr_old['head']['label'] == pr_new['head']['label']:
			send_comments(pr_old, pr_new['number'])
			break
pattern = re.compile("<(\S+)>; rel=\"next\"")
h = r.headers
print r.headers['X-RateLimit-Remaining']
result = pattern.search(h['link'])

while(result is not None):
	next_url = result.group(1)
 	r = requests.get(next_url, params = token, proxies = proxyDict)
	old_pr_list = r.json()
	for pr_old in old_pr_list:
		for pr_new in new_pr_list:
			if pr_old['head']['label'] == pr_new['head']['label']:
				send_comments(pr_old, pr_new['number'])
				break
	h = r.headers
	result = pattern.search(h['link'])
	