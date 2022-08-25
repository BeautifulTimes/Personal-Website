from flask import Flask
import time
import threading
import ast
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

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
        return 200

    pass

api.add_resource(feedback, '/feedback')  


if __name__ == '__main__':
    print("running")
    app.run()  # run our Flask app  