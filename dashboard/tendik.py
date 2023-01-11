from flask import Blueprint, request
from flask_restful import Api, Resource
from bson.json_util import dumps
from bson.objectid import ObjectId
from .db import get_tendiks, insert_tendik, get_user, get_tendik,update_tendik,delete_tendik
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import json

bp = Blueprint('tendik', __name__)
api = Api(bp)

class Guru_list(Resource):
    #@jwt_required()
    def get(self):
        data = get_tendiks({'status':'guru'})
        return json.loads(dumps(data))
    
    #@jwt_required()
    def post(self):
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            req = request.get_json()
            data = {
                'nama':req['nama'],
                'jenis_kelamin':req['jenis_kelamin'],
                'ttl':req['ttl'],
                'alamat':req['alamat'],
                'no_hp':req['no_hp'],
                'email':req['email'],
                'pendidikan_terakhir':req['pendidikan_terakhir'],
                'tahun_ajaran': req['tahun_ajaran'],
                'kelas_mengajar': req['kelas_mengajar'],
                'status':'guru'
            }
            insert_tendik(data)
            return{"success":True}
        else:
            return{"success":False, "msg":"only admin can perform this action"}




api.add_resource(Guru_list,'/API/tendik/guru')

class Tendik(Resource):
    #@jwt_required()
    def get(self, tendik_id):
        ObjInstance = ObjectId(tendik_id)
        filter = {'_id':ObjInstance}
        data = get_tendik(filter)
        return json.loads(dumps(data))
    
    #@jwt_required()
    def put(self, tendik_id):
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            ObjInstance = ObjectId(tendik_id)
            filter = {'_id':ObjInstance}
            req = request.get_json()
            newvalues = {"$set":{
                'nama':req['nama'],
                'jenis_kelamin':req['jenis_kelamin'],
                'ttl':req['ttl'],
                'alamat':req['alamat'],
                'no_hp':req['no_hp'],
                'email':req['email'],
                'pendidikan_terakhir':req['pendidikan_terakhir'],
                'tahun_ajaran': req['tahun_ajaran'],
                'kelas_mengajar': req['kelas_mengajar'],
                'status':req['status']
            }}
            update_tendik(filter, newvalues)
            return{"success":True}
        else:
            return{"success":False, "msg":"only admin can perform this action"}

    #@jwt_required()
    def delete(self, tendik_id):
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            ObjInstance = ObjectId(tendik_id)
            filter = {'_id':ObjInstance}
            delete_tendik(filter)
            return{"success":True}
        else:
            return{"success":False, "msg":"only admin can perform this action"}

api.add_resource(Tendik,'/API/tendik/<tendik_id>')

class NonGuru_list(Resource):
    #@jwt_required()
    def get(self):
        data = get_tendiks({'status':'non-guru'})
        return json.loads(dumps(data))
    
    #@jwt_required()
    def post(self):
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            req = request.get_json()
            data = {
                'nama':req['nama'],
                'jenis_kelamin':req['jenis_kelamin'],
                'ttl':req['ttl'],
                'alamat':req['alamat'],
                'no_hp':req['no_hp'],
                'email':req['email'],
                'pendidikan_terakhir':req['pendidikan_terakhir'],
                'tahun_ajaran': req['tahun_ajaran'],
                'kelas_mengajar': req['kelas_mengajar'],
                'status':'non-guru'
            }
            insert_tendik(data)
            return{"success":True}
        else:
            return{"success":False, "msg":"only admin can perform this action"}

api.add_resource(NonGuru_list,'/API/tendik/nonguru')
