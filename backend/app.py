from flask import Flask,  render_template, request, jsonify
from wtforms.validators import DataRequired
from wtforms import FileField, SubmitField
#from flask_wtf import FlaskForm
import pandas as pd
from chatterbot import ChatBot
from openai import OpenAI 
import pickle
import io
import os
from werkzeug.utils import secure_filename
import time
import math


#init the app
app = Flask(__name__)


## Declare ALL constants and hyper parameters
MODEL_PATH = 'models/stacking_model.pkl' # use absolute path
EXPECTED_FEATURES = ["koi_fpflag_nt","koi_fpflag_ss","koi_fpflag_co","koi_fpflag_ec","koi_period","koi_period_err1","koi_period_err2","koi_time0bk","koi_time0bk_err1","koi_time0bk_err2","koi_impact","koi_impact_err1","koi_impact_err2","koi_duration","koi_duration_err1","koi_duration_err2","koi_depth","koi_depth_err1","koi_depth_err2","koi_prad","koi_prad_err1","koi_prad_err2","koi_teq","koi_insol","koi_insol_err1","koi_insol_err2","koi_model_snr","koi_tce_plnt_num","koi_steff","koi_steff_err1","koi_steff_err2","koi_slogg","koi_slogg_err1","koi_slogg_err2","koi_srad","koi_srad_err1","koi_srad_err2","ra","dec","koi_kepmag","koi_tce_delivnameq1_q16_tce","koi_tce_delivnameq1_q17_dr24_tce","koi_tce_delivnameq1_q17_dr25_tce"]
#print(len(EXPECTED_FEATURES))
NASA_DEFAULT_DATA_PATH="static/ml/nasa_default.csv" # use absolute path




#Init chat bot
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
            

openai_apikey = 'sk-hDP__feS0PsrXdy22ncweQ' #use dotenv .env 
client = OpenAI(api_key=openai_apikey)
movie_bot = CustomChatBot('MovieBot')



class KeplerModel():

    def latest_run_to_json(self):
        # Only use confirmed exoplanets (self.latest_run)
        if not hasattr(self, 'latest_run') or not self.latest_run:
            return {}

        G = 6.67430e-11  # m^3 kg^-1 s^-2
        M_sun = 1.98847e30  # kg
        R_sun = 6.957e8  # m
        SECONDS_PER_DAY = 86400

        result = {}
        for row in self.latest_run:
            # Use KOI name or fallback to index
            name = row.get('kepoi_name') or row.get('kepid') or row.get('rowid') or f"KOI_{row.get('koi_name', 'unknown')}"

            # 1. Semi-major axis (a) in AU
            koi_period = float(row.get('koi_period', 0))  # days
            koi_steff = float(row.get('koi_steff', 5778))  # K
            koi_srad = float(row.get('koi_srad', 1))  # in solar radii
            koi_slogg = float(row.get('koi_slogg', 4.44))  # log10(cm/s^2)
            # Estimate stellar mass from logg and radius: M = g R^2 / G
            # logg is in cgs, so convert to m/s^2: g = 10**logg / 100
            g = 10 ** koi_slogg / 100.0
            R_star_m = koi_srad * R_sun
            M_star_kg = g * R_star_m**2 / G
            M_star_sun = M_star_kg / M_sun
            # Kepler's 3rd law (in AU): a = (P/365.25)^(2/3) * (M_star/M_sun)^(1/3)
            a = (abs(koi_period) / 365.25) ** (2/3) * (M_star_sun) ** (1/3) if koi_period > 0 else 1

            # 2. Eccentricity (e) - not directly available, set to 0 or estimate if possible
            e = float(row.get('koi_eccen', 0)) if 'koi_eccen' in row else 0.0

            # 3. Inclination (inc)
            koi_impact = float(row.get('koi_impact', 0))
            inc = None
            if a and koi_srad:
                try:
                    cosi = (koi_impact * koi_srad) / a
                    inc = math.degrees(math.acos(min(1, max(-1, cosi))))
                except Exception:
                    inc = 90.0
            else:
                inc = 90.0

            # 4. Node and Periapsis (not available, set to 0)
            node = 0.0
            peri = 90.0

            # 5. Mean anomaly (ma)
            koi_time0bk = float(row.get('koi_time0bk', 0))
            epoch = koi_time0bk
            ma = 0.0  # Could be calculated for a given epoch, but set to 0 for now

            # Extra params
            diameter = float(row.get('koi_prad', 1)) * 12742 / 2  # Earth radii to km (Earth diameter = 12742 km)
            risk = False
            impact = ""
            vel = 20.0
            years = 2025 # curernt year ?
            ip_max = 0.0
            ps_max = -5.0
            ts = 0
            ip_cum = 0.0
            ps_cum = -5.0
            obj_class = row.get('koi_disposition', 'CANDIDATE')
            obj_type = 'Exoplanet'

            result[name] = {
                "orbitParams": {
                    "epoch": epoch,
                    "a": a,
                    "e": e,
                    "inc": inc,
                    "node": node,
                    "peri": peri,
                    "ma": ma
                },
                "extraParams": {
                    "risk": risk,
                    "diameter": diameter,
                    "diameter_based_on_magnitude": True,
                    "impact": impact,
                    "IP max": ip_max,
                    "PS max": ps_max,
                    "TS": ts,
                    "vel": vel,
                    "years": years,
                    "IP cum": ip_cum,
                    "PS cum": ps_cum,
                    "class": obj_class,
                    "type": obj_type
                }
            }
        return result
    

    def __init__(self, *args, **kwargs):
        #Load and init Nasa Kepler model 
        
        self.latest_run:pd.DataFrame
        self.csv:pd.DataFrame = [] # initialise with empty or other default dataset
        #print(os.getpwd())
        with open(NASA_DEFAULT_DATA_PATH, 'r', encoding='utf-8') as f:
            self.csv = pd.read_csv(f)

        with open(MODEL_PATH, 'rb') as f:
            self.model = pickle.load(f)
        
    
    def predict(self):
        X = self.csv[EXPECTED_FEATURES] if all(col in self.csv.columns for col in EXPECTED_FEATURES) else self.csv
        X = X.fillna(X.median())

        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)

        # Add predictions and probabilities to the DataFrame
        df = self.csv.copy()
        df['prediction'] = predictions
        if probabilities.shape[1] > 1:
            df['prob_exoplanet'] = probabilities[:, 1]
        else:
            df['prob_exoplanet'] = probabilities[:, 0]

        # Split into two lists based on koi_disposition (1 = exoplanet, 0 = not)
        is_exploplanets = df[df['prediction'] == 1].to_dict(orient='records')
        is_not_exploplanets = df[df['prediction'] == 0].to_dict(orient='records')

        self.latest_run = is_exploplanets

        return is_exploplanets, is_not_exploplanets
    
    def update_csv(self,file):
        csv_data = file.read().decode('utf-8')
        csv = pd.read_csv(io.StringIO(csv_data))
        return
    
    def reset_csv(self):
        self.csv:pd.DataFrame = [] # initialise with empty or other default dataset
        with open(NASA_DEFAULT_DATA_PATH, 'r', encoding='utf-8') as f:
            self.csv = pd.read_csv(f)
        return   

kepler_model = KeplerModel()


#Helper fucntions definitions

# Landing page pre validation
def validate_csv(file):
        
    try:
        df=pd.read_csv(file,nrows=0)
    except pd.errors.ParserError:
        return False
    except FileNotFoundError:
        return False

    first_row = df.columns.tolist()
    for x in first_row:
        if(x not in EXPECTED_FEATURES):
            return False
        
    return True



#Defining all routes 


@app.route("/")
def Landing_pagefunction():
    return render_template( "index.html" )


@app.route('/validate_csv',methods=["POST"])
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
    if validate_csv(file) ==  False :
        print("cat3")
        return jsonify({"success": False, "message": "CSV validation failed"})
    
    kepler_model.update_csv(file)
    
    return jsonify({"success": True, "message": "CSV validated successfully"})



# API to call the Chatbot
@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    return str(movie_bot.get_response(user_text))


#API to call the Kepler model
@app.route("/kepler_predict")
def kepler_predict():
    # just call model and save results in object

    #time.sleep(20)
    kepler_model.predict()   
    #save result so that it can be read later by route /exoplanets
    #shoudl save them inside the kepler_model_obj


    return jsonify({"ok":True, "code":200 }) #status of request

@app.route("/use_default_dataset")
def use_default_dataset():

    kepler_model.reset_csv()

    return jsonify({"ok":True, "message": "it ran without crashing"})
 #redirect here or front end


#simulation of planets
@app.route("/simulation")
def simulation():
    return render_template( "orrery.html" )


@app.route("/exoplanets")
def get_exoplanets():

    #read result from models and convert  planets info in json following format beloew
    result_to_jsonify = kepler_model.latest_run_to_json()


    return jsonify(result_to_jsonify)
    """
    jsonify({
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
    """


@app.route("/loading")
def loading_page():
    return render_template("loading.html" )
