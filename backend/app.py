from flask import Flask,  render_template
from wtforms.validators import DataRequired
from wtforms import FileField, SubmitField
from flask_wtf import FlaskForm
import pandas

#init the app
app = Flask(__name__)



# Define the forms
class LoginForm(FlaskForm) :
    upload_csv = FileField('File', validators=[DataRequired()])
    submit = SubmitField("Submit")


def vcsvf(file):
        
    try:
        df=pd.read_csv(file,nrows=0)
    except pd.errors.ParserError:
        return False
    except FileNotFoundError:
        return False

    first_row = df.columns.tolist()
    words=[koi_fpflag_nt,koi_fpflag_ss,koi_fpflag_co,koi_fpflag_ec,koi_period,koi_period_err1,koi_period_err2,koi_time0bk,koi_time0bk_err1,koi_time0bk_err2,koi_impact,koi_impact_err1,koi_impact_err2,koi_duration,koi_duration_err1,koi_duration_err2,koi_depth,koi_depth_err1,koi_depth_err2,koi_prad,koi_prad_err1,koi_prad_err2,koi_teq,koi_insol,koi_insol_err1,koi_insol_err2,koi_model_snr,koi_tce_plnt_num,koi_steff,koi_steff_err1,koi_steff_err2,koi_slogg,koi_slogg_err1,koi_slogg_err2,koi_srad,koi_srad_err1,koi_srad_err2,ra,dec,koi_kepmag,koi_tce_delivnameq1_q16_tce,koi_tce_delivnameq1_q17_dr24_tce,koi_tce_delivnameq1_q17_dr25_tce,koi_disposition]
    for x in first_row:
        if(x not in words):
            return False
        
    return True
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

