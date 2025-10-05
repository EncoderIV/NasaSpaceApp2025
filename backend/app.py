from flask import Flask,  render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template( "orrery.html" )

@app.route("/home")
def Landing_pagefunction():
    return render_template( "index.html" )