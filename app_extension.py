import requests
import secrets
import json
import db

def getRepos(oauth_token, page=1):
	repos = []
	while len(repos) == 0:
		repos = json.loads(requests.get('https://api.github.com/user/repos?page=%s&sort=updated&affiliation=owner&' % page + oauth_token).text)
		repos = [rp for rp in repos if rp['permissions']['admin']]

		page -= 1
		if page < 1:
			break

	return repos

def tintRepo(oauth_token, reponame):
	# add tint webhook
	data = {}
	data['name'] = 'web'
	data['active'] = True
	data['events'] = ['push']
	data['config'] = { "url": "http://tintmyco.de:5000/webhook", "content_type": "form" } # TODO
	headers = {'content-type': 'application/json'}
	requests.post('https://api.github.com/repos/%s/hooks?%s' % (reponame, oauth_token),
		          data=json.dumps(data), headers=headers)

	# add tintapplication as collaborator
	headers = {'Content-Length': 0}
	requests.put('https://api.github.com/repos/%s/collaborators/tintapplication?%s' %
		         (reponame, oauth_token), headers=headers)

def untintRepo(oauth_token, full_reponame):
	# get rid of tint webhook
	r = requests.get('https://api.github.com/repos/%s/hooks?%s' % (full_reponame, oauth_token))
	json_result = json.loads(r.text)
	if isinstance(json_result, list):
		hooks = [hook['id'] for hook in json_result if hook['config']['url'] == 'http://tintmyco.de:5000/webhook']
		if len(hooks):
			hookid = hooks[0]

			# remove tint webhook
			headers = {'Content-Length': 0}
			requests.delete('https://api.github.com/repos/%s/hooks/%i?%s' %
			            	(full_reponame, hookid, oauth_token), headers=headers)

	# remove tintapplication as collaborator
	headers = {'Content-Length': 0}
	collab_url = 'https://api.github.com/repos/%s/collaborators/tintapplication?%s' % (full_reponame, oauth_token)
	r = requests.delete(collab_url, headers=headers)
	print r.text
