
#copy this script to your target repo
#run python github-stats.py to collect data
import re
import json
import os
import sys
import requests

#get token from cmd line
tk = sys.argv[1]

user_stats={"dummy":{"additions":0,"deletions":0,"total":0}}
#query github api for last year's commits
payload = {'since':'2013-01-01T00:00:00Z','until':'2014-01-01T00:00:00Z','access_token':tk}
token = {'access_token':tk}

def is_merge(commit_sha):
	cmd = "git show --oneline " + commit_sha
	output = os.popen(cmd)
	title = output.read()
	p_merge = re.compile("Merge")
	if(p_merge.search(title) is not None):
		return True
	else:
		return False

def collect_stats(commit_list):
	for m in commit_list:
		#print user_stats
		#print m['sha']

		#print data
		if(is_merge(m['sha'])):
			continue
		git_show_command = "git show -s --format=%an " + m['sha']
		
		output = os.popen(git_show_command)

		user = output.read().strip(' \t\n\r')
		#print user
		#r2 = requests.get(commit_request_api+m['sha'], params = token)
		#commit = r2.json()
		#print commit
		git_diff_command = "git diff --shortstat "+m['sha'] + " " + m['sha'] + "^"
		
		output = os.popen(git_diff_command)
		data = output.read()
		
		
		#print "data is:"
		#print data
		p_ins = re.compile("(\d+) insertion")

		r_ins = p_ins.search(data)

		ins_data = 0
		del_data = 0

		if(r_ins is not None):
		  ins_str = r_ins.group(1)
		  ins_data = int(ins_str)
		  #print ins_data

		p_del = re.compile("(\d+) deletion")

		r_del = p_del.search(data)

		if(r_del is not None):
		  del_str = r_del.group(1)
		  del_data = int(del_str)
		  #print del_data 

		if(ins_data + del_data > 5000):
		  print user
		  print 'ins:'+str(ins_data)
		  print 'del:'+str(del_data)
		  ins_data = 0
		  del_data = 0
		if(user in user_stats):
		  stats = user_stats[user]
		  stats['additions'] += ins_data
		  stats['deletions'] += del_data
		  stats['total'] += (ins_data + del_data)
		  user_stats[user] = stats
		else:
		  new_stat = {'additions':ins_data, 'deletions':del_data, 'total':ins_data+del_data}
		  user_stats[user] = new_stat

r = requests.get("https://api.github.com/repos/cocos2d/cocos2d-x/commits", params = payload)
collect_stats(r.json())

print user_stats

pattern = re.compile("<(\S+)>; rel=\"next\"")
h = r.headers
print r.headers['X-RateLimit-Remaining']
result = pattern.search(h['link'])

while(result is not None):
	
	next_url = result.group(1)
 	r = requests.get(next_url, params = token)

	collect_stats(r.json())
  

	h = r.headers
	print h['link']
	result = pattern.search(h['link'])

	#print h['link']
	#next_url = result.group(1)
	#print next_url
	#r_next = requests.get(next_url[1])

	print r.headers['X-RateLimit-Remaining']
	print user_stats
