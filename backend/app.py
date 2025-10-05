from flask import Flask,  render_template, request, jsonify
from chatterbot import ChatBot
from openai import OpenAI 


#initialising stuff
app = Flask(__name__)

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
            

openai_apikey = 'sk-hDP__feS0PsrXdy22ncweQ'
client = OpenAI(api_key=openai_apikey)
# Create a new chatbot
movie_bot = CustomChatBot('MovieBot')

#Defining all routes 
@app.route("/")
def hello_world():
    return render_template( "orrery.html" )


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