from flask import Flask, render_template, request
import json

app = Flask(__name__)
app.secret_key = "blerp derp"

@app.route('/', methods=['GET', 'POST'])
def home():
	print json.loads(request.data)
	return "AY"

if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)
