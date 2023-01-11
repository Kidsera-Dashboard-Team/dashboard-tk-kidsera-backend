import json
from bson.json_util import dumps
from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import *
from bson.objectid import ObjectId
from .db import *

bp = Blueprint('rombel', __name__)
api = Api(bp)

class Rombel(Resource):
    #@jwt_required()
    def get(self, rombel_id):
        id = ObjectId(rombel_id)
        rombel = get_rombel(id)

        tahun_ajaran = rombel['tahun_ajaran']
        kelas = rombel['kelas']
        ruangan = rombel['ruangan']

        filter_siswa = {"tahun_ajaran" : tahun_ajaran, "tingkat_kelas" : kelas}
        filter_tendik = {"tahun_ajaran" : tahun_ajaran, "kelas_mengajar" : kelas}

        list_siswa = json.loads(dumps(getAll_student(filter_siswa)))
        wali_kelas = json.loads(dumps(get_tendik(filter_tendik)))

        data = {"list_siswa" : list_siswa, "wali_kelas" : wali_kelas, "ruangan" : ruangan}
        return data

    #@jwt_required()
    def put(self, rombel_id):
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            id = ObjectId(rombel_id)
            filter = {"_id":id}

            if get_rombel(filter) is None: 
                return {"Success" : False, "msg" : "Id not valid"}
            else:
                req = request.get_json()
                new_val = {
                    "$set":{
                        "tahun_ajaran" : req['tahun_ajaran'],
                        "kelas" : req['kelas'],
                        "ruangan" : req['ruangan'],
                    }
                }
                update_rombel(filter, new_val)
                return {"Success" : True, "msg" : "Data has been updated"}
        else:
            return {"Success" : False, "msg" : "Only admin can perform this action"}

api.add_resource(Rombel, "/API/rombel/<rombel_id>")

class Rombels(Resource):
    #@jwt_required()
    def get(self):
        data = get_tahun_ajaran()
        datas = [x['tahun_ajaran'] for x in data]
        datas1 = list(set(datas))
        datas1.sort()
        return json.loads(dumps(datas1)) 

    #@jwt_required()
    def post(self):
        # email = get_jwt_identity()
        # userDetail = get_user({"email":email})
        # if userDetail['is_admin']:
        req = request.get_json()
        data = {
            "tahun_ajaran" : req['tahun_ajaran'],
            "kelas" : req['kelas'],
            "ruangan" : req['ruangan']
        }
        insert_rombel(data)
        return {"Success" : True, "msg" : "New rombel successfully added"}
        # else:
        #     return {"Success" : False, "msg" : "Only admin can perform this action"}

api.add_resource(Rombels, "/API/rombel")

class Rombelget(Resource):
    def get(self, year, classes):
        yearFormat = '/'.join(year.split('-'))
        filter = {"tahun_ajaran":yearFormat, "kelas":classes}

        rombel = get_rombel(filter)

        filter_siswa = {"tahun_ajaran" : yearFormat, "tingkat_kelas" : classes}
        filter_tendik = {"tahun_ajaran" : yearFormat, "kelas_mengajar" : classes}

        list_siswa = json.loads(dumps(getAll_student(filter_siswa)))
        wali_kelas = json.loads(dumps(get_tendik(filter_tendik)))

        data = {"list_siswa" : list_siswa, "wali_kelas" : wali_kelas,"rombel":rombel}
        
        return json.loads(dumps(data)) 

    
    def put(self, year, classes):
        yearFormat = '/'.join(year.split('-'))
        filter = {"tahun_ajaran":yearFormat, "kelas":classes}
        rombel = get_rombel(filter)

        if get_rombel(filter) is None: 
            return {"Success" : False, "msg" : "Id not valid"}
        else:
            req = request.get_json()
            new_val = {
                "$set":{
                    "tahun_ajaran" : req['tahun_ajaran'],
                    "kelas" : req['kelas'],
                    "ruangan" : req['ruangan'],
                }
            }
            update_rombel(filter, new_val)
            return {"Success" : True, "msg" : "Data has been updated"}
        

api.add_resource(Rombelget, "/API/rombel/<year>/<classes>")

        