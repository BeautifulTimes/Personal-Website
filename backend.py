from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from flask import Flask
import ast
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import os
import openai
app = Flask(__name__)
api = Api(app)
CORS(app)
curuser = -1
allconversations = []
numberofmessages = []
session = Session(profile_name="default")
polly = session.client("polly")
def saysomething(input,counter):
    try:
        response = polly.synthesize_speech(Text=input, OutputFormat="mp3",
                                        VoiceId="Joanna")
    except (BotoCoreError, ClientError) as error:
        print(error)
        sys.exit(-1)

    if "AudioStream" in response:
        numberofmessages[counter] = numberofmessages[counter]+1
        file = open("sounds/" + str(numberofmessages[counter]) + '_' + str(counter) + 'speech.mp3', 'wb')
        file.write(response['AudioStream'].read())
        file.close()
    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)
class feedback(Resource):
    def get(self):
        global curuser
        global allconversations
        curuser = curuser + 1
        allconversations.append([{"role": "system", "content": "I want you to act as an accredited therapist. I will give you words from the patient and you will respond as a therapist. Your name is amy.Do not use any special escape charchters in your response"}])
        numberofmessages.append(0)
        print(curuser)
        return curuser , 200
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('feedback')
        parser.add_argument('userid')
        args = parser.parse_args()     
        print(args['feedback'])
        print(args['userid'])
        userid =  int(args['userid'])
        if(userid > curuser):
            return "something went wrong"
        openai.api_key = os.getenv("OPENAI_API_KEY")
        allconversations[userid].append({"role": "user", "content": args['feedback']})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=  allconversations[userid]
        )
        responsetext = response["choices"][0]["message"]["content"]
        responsetext = responsetext.strip()
        saysomething(responsetext,userid)
        allconversations[userid].append({"role": "assistant", "content": responsetext})
        return responsetext
    pass

api.add_resource(feedback, '/feedback')  


if __name__ == '__main__':
    print("running")
    app.run()  # run our Flask app  