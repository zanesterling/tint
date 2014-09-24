import requests
import secrets
import json
import db

def getRepos(oauth_token):
	repos = json.loads(requests.get('https://api.github.com/user/repos?' + oauth_token).text)
	repos = [rp for rp in repos if rp['permissions']['admin']]
	return repos

def tintRepo(username, oauth_token, reponame):
	# add tint webhook
	data = {}
	data['name'] = 'web'
	data['active'] = True
	data['events'] = ['push']
	data['config'] = { "url": "http://104.131.55.76:5000/webhook", "content_type": "form" } # TODO
	headers = {'content-type': 'application/json'}
	requests.post('https://api.github.com/repos/%s/%s/hooks?%s' % (username, reponame, oauth_token),
		          data=json.dumps(data), headers=headers)

	# add tintapplication as collaborator
	headers = {'Content-Length': 0}
	requests.put('https://api.github.com/repos/%s/%s/collaborators/tintapplication?%s' %
		         (username, reponame, oauth_token), headers=headers)

def untintRepo(username, oauth_token, reponame):
	# get id of tint webhook
	r = requests.get('https://api.github.com/repos/%s/%s/hooks?%s' % (username, reponame, oauth_token))
	hooks = [hook['id'] for hook in json.loads(r.text)
		     if hook['config']['url'] == 'http://104.131.55.76:5000/webhook']
	if len(hooks):
		hookid = hooks[0]

		# remove tint webhook
		headers = {'Content-Length': 0}
		requests.delete('https://api.github.com/repos/%s/%s/hooks/%i?%s' %
			            (username, reponame, hookid, oauth_token), headers=headers)

	# add tintapplication as collaborator
	headers = {'Content-Length': 0}
	requests.delete('https://api.github.com/repos/%s/%s/collaborators/tintapplication?%s' %
		            (username, reponame, oauth_token), headers=headers)
