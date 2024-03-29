from flask import Flask
import time
import threading
import ast
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
points = 0
savetime = 10
scoreboardrefresh = 10
app = Flask(__name__)
api = Api(app)
CORS(app)
scoredata = {}
userdata = {}
scoreboard = []
javastring = ""
def invalidname(name):
    useless = 0
    if len(name) < 2 or len(name) > 32:
        return True
    for chars in name:
        if (chars <= 'Z' and chars >= 'A') or (chars <= 'z' and chars >= 'a') or (chars <= '9' and chars >= '0') or (chars == ' '):
            useless = useless + 1
        else:
            return True
    return False
def savedata():
    while 1==1:
        time.sleep(savetime)
        f = open("savedata.txt","w")
        f.write(str(userdata))
        f.write("\n")
        f.write(str(scoredata))
        f.close() #to change file access modes
def readsavedata():
    global userdata
    global scoredata
    f = open("savedata.txt", "r")
    userdata = ast.literal_eval(f.readline())
    scoredata = ast.literal_eval(f.readline())
    f.close()
def sortinfunc(e):
    return e[1] * 100000 - e[2]/1000000000000 
def updatescoreboard():
    while 1==1:
        global scoreboard
        global javastring
        javastring = ""
        scoreboard = []
        for key in scoredata:
            scoreboard.append((key,len(scoredata[key])-1,scoredata[key]['time']))
        scoreboard.sort(key=sortinfunc, reverse=True)
        maxnumber = 0
        for item in scoreboard:
            maxnumber = maxnumber + 1
            javastring = javastring + str(item[0]) + "," + str(item[1]) + ","
            if maxnumber > 10:
                break
        time.sleep(scoreboardrefresh)
class Users(Resource):
    def get(self):
        global points   
        points = points + 1
        return javastring , 200
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('username')
        parser.add_argument('value')
        args = parser.parse_args()  # parse arguments to dictionary
        if args['username'] in userdata:
            if args['value'] not in scoredata[args['username']]:
                print(args['username'])
                scoredata[args['username']][args['value']] = 1
                scoredata[args['username']]['time'] = time.time() 
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
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('user')
        args = parser.parse_args()  # parse arguments to dictionary
        if args['user'] in userdata:    
            return 200
        else:
            return 512
    pass
class getselfpoint(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('user')
        args = parser.parse_args()  # parse arguments to dictionary
        if args['user'] in userdata:    
            return len(scoredata[args['user']])-1
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
        namecheck = args['user']
        if invalidname(namecheck):
            return 513
        if args['user'] == "":
            return 513
        if args['user'] not in userdata:
            userdata[args['user']] = 1
            scoredata[args['user']] = {}
            scoredata[args['user']]['time'] = time.time()
            return 200
        else:
            return 512
        print(args)

    pass

api.add_resource(Users, '/users')  
api.add_resource(login, '/login') 
api.add_resource(register, '/register') 
api.add_resource(getselfpoint, '/getselfpoint') 


readsavedata()
axxx2 = threading.Thread(target=savedata, args=())

axxx = threading.Thread(target=updatescoreboard, args=())
axxx.start()
axxx2.start()
if __name__ == '__main__':
    print("running")
    app.run()  # run our Flask app  