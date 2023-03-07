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

class feedback(Resource):
    def get(self):
        return userdata , 200
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('feedback')
        args = parser.parse_args()  # parse arguments to dictionary       
        print(args['feedback'])
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Create a 500 word Essay on the following target:\n" + args['feedback'],
        temperature=0.7,
        max_tokens=600,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
        print(response);
        print(type(response))
        responsetext = response["choices"][0]["text"]
        responsetext = responsetext.strip()
        return responsetext
    pass

api.add_resource(feedback, '/feedback')  


if __name__ == '__main__':
    print("running")
    app.run()  # run our Flask app  