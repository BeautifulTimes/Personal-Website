from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
points = 0
app = Flask(__name__)
api = Api(app)
CORS(app)

class Users(Resource):
    def get(self):
        global points
      #  print(points)
        points = points + 1
        return points , 200
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        args = parser.parse_args()  # parse arguments to dictionary
        print(args)
        global points
        points = 1000
       
    pass

api.add_resource(Users, '/users')  # '/users' is our entry point
if __name__ == '__main__':
    print("running")
    app.run()  # run our Flask app