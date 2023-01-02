
from flask import Blueprint,current_app,request,jsonify
from.db import insert_user, get_user, block_token
from flask_restful import Api, Resource
from hashlib import md5
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import datetime

bp = Blueprint('auth', __name__)
api = Api(bp)

class Register(Resource):
    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            req = request.get_json()
            email = req['email']
            username = req['username']
            if get_user({'email':email}) == None and get_user({'username': username}) == None:
                data = {'email' : email,
                'username' : username,
                'password' : md5(req['password'].encode('utf-8')).hexdigest(),
                'first_name' : req['fname'],
                'last_name' : req['lname'],
                'is_admin': False}
                insert_user(data)
                return {'success':True}
            elif get_user({'email':email}) == None:
                return{'success':False,'message': 'email is already used'}
            else:
                return{'success':False,'message': 'username is already used'}
        else:
            return{"success":False, "msg":"only admin can perform this action"}
        

api.add_resource(Register,'/API/auth/register')

class Login(Resource):
    def post(self):
        req = request.get_json()
        username = req['username']
        password = md5(req['password'].encode('utf-8')).hexdigest()
        data = get_user({'username':username})
        if data is not None:
            if data['password']==password:
                access_token = create_access_token(identity=username)
                return {'success':True,'access_token': access_token, 'is_admin': data['is_admin'], 'username' : data['username']}
            else:
                return {'success':False, 'message':'wrong password or username'}
        else:
            return {'success':False, 'message':'wrong username'}
        

api.add_resource(Login,'/API/auth/login')


class Logout(Resource):
    @jwt_required()
    def delete(self):
        jti = get_jwt()['jti']
        current_time = datetime.datetime.now()
        block_token({'jti':jti, 'created_at':current_time})
        return {'success': True, 'msg':'logout success'}


api.add_resource(Logout,'/API/auth/logout')

class CreateAdmin(Resource):
    @jwt_required()
    def post(self):
        req = request.get_json()
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            email = req['email']
            username = req['username']
            if get_user({'email':email}) == None and get_user({'username': username}) == None:
                data = {'email' : email,
                'username' : username,
                'password' : md5(req['password'].encode('utf-8')).hexdigest(),
                'first_name' : req['fname'],
                'last_name' : req['lname'],
                'is_admin': True}
                insert_user(data)
                return {'success':True}
            elif get_user({'email':email}) == None:
                return{'success':False,'message': 'email is already used'}
            else:
                return{'success':False,'message': 'username is already used'}
        else:
            return{"success":False, "msg":"only admin can perform this action"}

api.add_resource(CreateAdmin,'/API/auth/createadmin')


        
