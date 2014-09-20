import requests
import secrets
import json
import db

def getRepos(username, oauth_token):
	params = {}
	params['type'] = 'owner'
	params['client_id'] = secrets.client_id
	params['client_secret'] = secrets.client_secret

	for attr in oauth_token.split('&'):
		attr = attr.split('=')
		params[attr[0]] = attr[1]

	r = requests.get('https://api.github.com/users/%s/repos' % username, params=params)
	return json.loads(r.text)
