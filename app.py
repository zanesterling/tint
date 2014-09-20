from flask import Flask, render_template, request, session, redirect, url_for
from app_extension import *
import requests as pyrequests
import secrets
import json
import db

app = Flask(__name__)
app.secret_key = "blerp derp"

@app.route('/')
def home():
	d = {}
	d['client_id'] = secrets.client_id
	if not 'github_token' in session:
		d['logged_in'] = False
		return render_template("welcome.html", d=d)

	d['logged_in'] = True
	d['username'] = session['username']
	d['repos'] = getRepos(session['username'], session['github_token'])
	return render_template("home.html", d=d)

# process github's oauth callback and add user as necessary
@app.route('/oauth-callback')
def oauth_callback():
	data = {}
	data["client_id"] = secrets.client_id
	data["client_secret"] = secrets.client_secret
	data["code"] = request.args.get("code")
	oauth_token = pyrequests.post('https://github.com/login/oauth/access_token', data).text

	# check if user exists already, and update or add them to the db accordingly
	response = pyrequests.get('https://api.github.com/user?' + oauth_token).text
	resp_dict = json.loads(response)
	if 'login' in resp_dict:
		session['github_token'] = oauth_token
		username = resp_dict['login']
		session['username'] = username
		if db.userExists(username):
			db.updateUser(username, oauth_token)
		else:
			db.createUser(username, oauth_token)

	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	if 'github_token' in session:
		del session['github_token']
	if 'username' in session:
		del session['username']
	return redirect(url_for('home'))

@app.route('/client-callback')
def clientCallback():
	if request.args.get('action') == 'tint':
		tintRepo(request.args.['username'], session['oauth_token'], request.args.['repo'])

if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)
