import re
import json
import requests
import traceback

tk = 'a135a2fbce040b1988225f1c72d021fe5b90d07e'
token = {'access_token':tk}

http_proxy = 'http://127.0.0.1:8087'
proxyDict = {'http':http_proxy,'https':http_proxy}

target_repo = 'https://api.github.com/repos/cocos2d/cocos2d-x-classic/'
src_repo = 'https://api.github.com/repos/cocos2d/cocos2d-x/'
target_branch = 'v3'
src_branch = 'v3'

def send_pull_reqeust(pr):
	Headers = {"Authorization":"token " + tk} 
	try:
		print pr
		requests.post(target_repo + 'pulls', data = json.dumps(pr), headers = Headers, proxies = proxyDict)
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

target_pr_list = get_all_pr(target_repo, target_branch)
r = requests.get(src_repo+'pulls?base='+src_branch, params = token, proxies = proxyDict)
pr_list = r.json()
print len(pr_list)
idx = 0
for pr in pr_list:
	print idx
	idx += 1
	_pr = {}
	_pr['title'] = '[ci skip]' + pr['title']
	_pr['body'] = pr['body']
	_pr['head'] = pr['head']['label']
	_pr['base'] = target_branch
	_found = False
	for pr_target in target_pr_list:
		if _pr['head'] == pr_target['head']['label']:
			_found = True
			break
	if _found is False:
		send_pull_reqeust(_pr)
	else:
		print _pr['title'] + 'is already created'
pattern = re.compile("<(\S+)>; rel=\"next\"")
h = r.headers
print r.headers['X-RateLimit-Remaining']
result = pattern.search(h['link'])

while(result is not None):
	
	next_url = result.group(1)
 	r = requests.get(next_url, params = token, proxies = proxyDict)

	#collect_stats(r.json())
	pr_list = r.json()
	print len(pr_list)
	idx = 0
  	for pr in pr_list:
  		print idx
  		idx += 1
		_pr = {}
		_pr['title'] = '[ci skip]' + pr['title']
		_pr['body'] = pr['body']
		_pr['head'] = pr['head']['label']
		_pr['base'] = target_branch
		_found = False
		for pr_target in target_pr_list:
			if _pr['head'] == pr_target['head']['label']:
				_found = True
				break
		if _found is False:
			send_pull_reqeust(_pr)
		else:
			print _pr['title'] + 'is already created'
	h = r.headers
	print h['link']
	result = pattern.search(h['link'])

	#print h['link']
	#next_url = result.group(1)
	#print next_url
	#r_next = requests.get(next_url[1])

	print r.headers['X-RateLimit-Remaining']
	#print user_stats
