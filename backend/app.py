from flask import Flask,  render_template, request
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