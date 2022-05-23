from flask import Flask
import time
import threading
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
points = 0
savetime = 60
app = Flask(__name__)
api = Api(app)
CORS(app)
scoredata = {}
userdata = {}
def savedata():
    while 1==1:
        time.sleep(savetime * 1000)
        f = open("savedata.txt","w")
        f.write(userdata)
        f.write("/n")
        f.write(scoredata)
        f.close() #to change file access modes
class Users(Resource):
    def get(self):
        global points   
        points = points + 1
        return scoredata , 200
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('username')
        parser.add_argument('value')
        args = parser.parse_args()  # parse arguments to dictionary
        print(args['username'])
        if args['username'] in userdata:
            if args['value'] not in scoredata[args['username']]:
                scoredata[args['username']][args['value']] = 1 
            else:
                return 512

        else:
            return 512
        return 200
       
    pass
class login(Resource):
    def get(self):
        return userdata , 200
    def post(self):
        print('running')
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('user')
        args = parser.parse_args()  # parse arguments to dictionary
        if args['user'] in userdata:    
            return 200
        else:
            return 512
    pass
class register(Resource):
    def get(self):
        return userdata , 200
    def post(self):
        print('running')
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('user')
        args = parser.parse_args()  # parse arguments to dictionary
        if args['user'] not in userdata:
            userdata[args['user']] = 1
            scoredata[args['user']] = {}
            return 200
        else:
            return 512
        print(args)
    pass
api.add_resource(Users, '/users')  # '/users' is our entry point
api.add_resource(login, '/login')  # '/users' is our entry point
api.add_resource(register, '/register')  # '/users' is our entry point
threading.thread.start_new_thread( print_time())
if __name__ == '__main__':
    print("running")
    app.run()  # run our Flask app