from flask import Flask,  render_template

#initialising stuff
app = Flask(__name__)

#Defining all routes 
@app.route("/")
def hello_world():
    return render_template( "orrery.html" )