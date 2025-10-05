from flask import Flask,  render_template, request, jsonify
from wtforms.validators import DataRequired
from wtforms import FileField, SubmitField
from flask_wtf import FlaskForm
from flask import Flask, request, jsonify, render_template
import pandas as pd
from chatterbot import ChatBot
from openai import OpenAI 

#init the app
app = Flask(__name__)



# Define and init bunch of stuff
class LoginForm(FlaskForm) :
    upload_csv = FileField('File', validators=[DataRequired()])
    submit = SubmitField("Submit")


class CustomChatBot(ChatBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_response(self, statement, **kwargs):
        # Add your custom logic here before or after calling the parent method

        # Make a request to the OpenAI API
        try :  
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": statement}
                ]
            )
            if completion :
                return completion.choices[0].message
            else :
                return "Sorry could not help at the moment. Please try again later."
        except Exception as e:
            # Handle other unexpected errors
            return "Sorry could not help at the moment. Please try again later."
            

# Create a new chatbot
openai_apikey = 'sk-hDP__feS0PsrXdy22ncweQ' #use dotenv .env
client = OpenAI(api_key=openai_apikey)
movie_bot = CustomChatBot('MovieBot')




def validate_csv(file):
        
    try:
        df=pd.read_csv(file,nrows=0)
    except pd.errors.ParserError:
        return False
    except FileNotFoundError:
        return False

    first_row = df.columns.tolist()
    words=["koi_fpflag_nt","koi_fpflag_ss","koi_fpflag_co","koi_fpflag_ec","koi_period","koi_period_err1","koi_period_err2","koi_time0bk","koi_time0bk_err1","koi_time0bk_err2","koi_impact","koi_impact_err1","koi_impact_err2","koi_duration","koi_duration_err1","koi_duration_err2","koi_depth","koi_depth_err1","koi_depth_err2","koi_prad","koi_prad_err1","koi_prad_err2","koi_teq","koi_insol","koi_insol_err1","koi_insol_err2","koi_model_snr","koi_tce_plnt_num","koi_steff","koi_steff_err1","koi_steff_err2","koi_slogg","koi_slogg_err1","koi_slogg_err2","koi_srad","koi_srad_err1","koi_srad_err2","ra","dec","koi_kepmag","koi_tce_delivnameq1_q16_tce","koi_tce_delivnameq1_q17_dr24_tce","koi_tce_delivnameq1_q17_dr25_tce","koi_disposition"]
    for x in first_row:
        if(x not in words):
            return False
        
    return True








#Defining all routes 


@app.route("/")
def hello_world():
    return render_template( "orrery.html" )

@app.route("/home")
def Landing_pagefunction():
    return render_template( "index.html" )


@app.route('/loading',methods=["POST"])
def loading():
    # Do training/prediction here
   # run_training_or_prediction()
    # When done, redirect to /simulation
    #return redirect(url_for(''))
    if "file" not in request.files:
        print("cat1")
        return jsonify({"success": False, "message": "No file uploaded"})
        

    file = request.files["file"]
    if file.filename == "":
        print("cat2")
        return jsonify({"success": False, "message": "No selected file"})


    # Run validation
    if validate_csv(file):
        print("cat3")
        return jsonify({"success": True, "message": "CSV validated successfully"})
    else:
        print("cat4")
        return jsonify({"success": False, "message": "CSV validation failed"})



@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    return str(movie_bot.get_response(user_text))



@app.route("/exoplanets")
def get_exoplanets():
    # test for plug and play once model is connected
    # will just call mdodel or read database here
    #and format here or before hand
    return jsonify({
        "(2023 VD3)": {
            "orbitParams": {
                "epoch": 60600,
                "a": 1.351737253,
                "e": 0.557073461,
                "inc": 11.84982014,
                "node": 46.01796989,
                "peri": 95.91669242,
                "ma": 181.950708
            },
            "extraParams": {
                "risk": True,
                "diameter": 14.0,
                "diameter_based_on_magnitude": True,
                "impact": "08/11/2034 17:09",
                "IP max": 0.00258,
                "PS max": -2.65,
                "TS": 0,
                "vel": 21.01,
                "years": "2034-2098",
                "IP cum": 0.00258,
                "PS cum": -2.65,
                "class": "APO",
                "type": "NEA"
            }
        },
        "(1979 XB)": {
            "orbitParams": {
                "epoch": 60600,
                "a": 2.567881579,
                "e": 0.746345087,
                "inc": 25.30872181,
                "node": 81.55419175,
                "peri": 78.85896163,
                "ma": 336.878152
            },
            "extraParams": {
                "risk": True,
                "diameter": 500.0,
                "diameter_based_on_magnitude": True,
                "impact": "12/12/2056 21:38",
                "IP max": 2.34e-07,
                "PS max": -2.84,
                "TS": 0,
                "vel": 27.54,
                "years": "2056-2113",
                "IP cum": 7.34e-07,
                "PS cum": -2.72,
                "class": "APO",
                "type": "NEA"
            }
        }
    })
