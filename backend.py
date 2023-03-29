from flask import Flask
import time
import threading
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
class feedback(Resource):
    def get(self):
        global curuser
        global allconversations
        curuser = curuser + 1
        allconversations.append([{"role": "system", "content": "You are Amy, a certified psychologist and therapist. Respond to me as amy."}])
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
        openai.api_key = os.getenv("OPENAI_API_KEY")
        allconversations[userid].append({"role": "user", "content": args['feedback']})
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=  allconversations[userid]
        )
        responsetext = response["choices"][0]["message"]["content"]
        responsetext = responsetext.strip()
        allconversations[userid].append({"role": "assistant", "content": responsetext})
        return responsetext
    pass

api.add_resource(feedback, '/feedback')  


if __name__ == '__main__':
    print("running")
    app.run()  # run our Flask app  