from flask import Flask, render_template, request
import json
import secrets

app = Flask(__name__)
app.secret_key = "blerp derp"

@app.route('/', methods=['GET', 'POST'])
def home():
	print json.loads(request.data)
	d = {'client-id': secrets.client_id}
	return render_template("home.html", d=d)

if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)
