from flask import Flask, render_template
import secrets

app = Flask(__name__)
app.secret_key = "blerp derp"

@app.route('/')
def home():
	d = {'client-id': secrets.client_id}
	return render_template("home.html", d=d)

if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)
