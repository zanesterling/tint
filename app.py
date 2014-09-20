from flask import Flask, render_template, request, session, redirect, url_for
import requests as pyrequests
import secrets

app = Flask(__name__)
app.secret_key = "blerp derp"

@app.route('/')
def home():
	d = {}
	d['client_id'] = secrets.client_id
	d['logged_in'] = 'github_token' in session
	return render_template("home.html", d=d)

# process github's oauth callback and add user as necessary
@app.route('/oauth-callback')
def oauth_callback():
	data = {}
	data["client_id"] = secrets.client_id
	data["client_secret"] = secrets.client_secret
	data["code"] = request.args.get("code")
	r = pyrequests.post('https://github.com/login/oauth/access_token', data)
	session['github_token'] = r.text

	# TODO check if user exists already, and if not set up all da jazz

	return redirect(url_for('home'))

if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)
