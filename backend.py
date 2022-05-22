from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
points = 0
app = Flask(__name__)
api = Api(app)
CORS(app)
scoredata = {}
userdata = {}
class Users(Resource):
    def get(self):
        global points   
        points = points + 1
        return dictdata , 200
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('username')
        parser.add_argument('value')

        args = parser.parse_args()  # parse arguments to dictionary
        if args['username'] in userdata:
            if args['values'] not in scoredata[args['username']]:
                scoredata[args['username']][args['values']] = 1 
        else:
            return 512
        print(args)
       
    pass
class login(Resource):
    def get(self):
        global points   
        points = points + 1
        return dictdata , 200
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('user')
        parser.add_argument('password')
        args = parser.parse_args()  # parse arguments to dictionary
        if args['name'] not in dictdata:
            userdata[args['name']] = args['password']
            scoredata['name'] = {}
        else:
            return 512
        print(args)
       
    pass
api.add_resource(Users, '/users')  # '/users' is our entry point
api.add_resource(login, '/login')  # '/users' is our entry point

if __name__ == '__main__':
    print("running")
    app.run()  # run our Flask app