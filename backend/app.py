from flask import Flask,  render_template
from wtforms.validators import DataRequired
from wtforms import FileField, SubmitField
from flask_wtf import FlaskForm

#init the app
app = Flask(__name__)



# Define the forms
class LoginForm(FlaskForm) :
    upload_csv = FileField('File', validators=[DataRequired()])
    submit = SubmitField("Submit")



#Define Routes

@app.route("/")
def hello_world():
    return render_template( "orrery.html" )

@app.route("/home")
def Landing_pagefunction():
    return render_template( "index.html" )

@app.route('/loading')
def loading():
    # Do training/prediction here
    run_training_or_prediction()
    # When done, redirect to /simulation
    return redirect(url_for(''))

