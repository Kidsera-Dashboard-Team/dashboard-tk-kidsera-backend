import json
from bson.json_util import dumps
from flask import Blueprint, request

from .db import *

from bson.objectid import ObjectId
from flask_restful import Api, Resource
from flask_jwt_extended import *

bp = Blueprint('students',__name__)
api = Api(bp)

class Students(Resource):
    #@jwt_required()
    def get(self):
        data = getAll_student()
        return json.loads(dumps(data))
    
    #@jwt_required()
    def post(self):
        # email = get_jwt_identity()
        # userDetail = get_user({"email":email})
        # if userDetail['is_admin']:
        req = request.get_json()
        data = {
            'nama' : req['nama'],
            'status' : req['status'],
            'jenis_kelamin' : req['jenis_kelamin'], 
            'tahun_ajaran' : req['tahun_ajaran'],
            'nik' : req['nik'], 
            'nisn' : req['nisn'], 
            'no_kk' : req['no_kk'], 
            'tingkat_kelas' : req['tingkat_kelas'], 
            'tanggal_masuk' :req['tanggal_masuk'],
            'tanggal_lulus' :req['tanggal_lulus'],
            'nomor_induk' : req['nomor_induk'],
            'tinggi_badan' : int(req['tinggi_badan']),
            'berat_badan' : int(req['berat_badan']),
            'lingkar_kepala' : int(req['lingkar_kepala']),
            'alergi' : req['alergi'],
            'nama_ayah' : req['nama_ayah'],
            'nama_ibu' : req['nama_ibu'],
            'pekerjaan_ayah' : req['pekerjaan_ayah'],
            'pekerjaan_ibu' : req['pekerjaan_ibu'],
            'no_telp_ayah' : req['no_telp_ayah'],
            'no_telp_ibu' : req['no_telp_ibu']
        }
        insert_student(data)
        return {'Success': True}
        # else:
        #     return {"Success" : False, "msg" : "Only admin can perform this action"}

api.add_resource(Students, '/API/students')

class Student(Resource):
    #@jwt_required()
    def get(self, student_id):
        id = student_id
        ObjInstance = ObjectId(id)
        filter = {'_id' : ObjInstance}
        data = get_student(filter)
        return json.loads(dumps(data))
    
    #@jwt_required()
    def put(self, student_id):
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            ObjInstance = ObjectId(student_id)
            filter = {'_id':ObjInstance}
            if (get_student(filter) is None):
                return {"message":"ID not valid"}
            else:
                req = request.get_json()
                newVal = {
                    "$set":{
                        'nama' : req['nama'],
                        'jenis_kelamin' : req['jenis_kelamin'], 
                        'nisn' : req['nisn'], 
                        'nik' : req['nik'], 
                        'no_kk' : req['no_kk'], 
                        'tingkat_kelas' : req['tingkat_kelas'], 
                        'tanggal_masuk' :req['tanggal_masuk'],
                        'tanggal_lulus' :req['tanggal_lulus'],
                        'nomor_induk' : req['nomor_induk'],
                        'status' : req['status'],
                        'tinggi_badan' : int(req['tinggi_badan']),
                        'berat_badan' : int(req['berat_badan']),
                        'lingkar_kepala' : int(req['lingkar_kepala']),
                        'alergi' : req['alergi'],
                        'nama_ayah' : req['nama_ayah'],
                        'nama_ibu' : req['nama_ibu'],
                        'pekerjaan_ayah' : req['pekerjaan_ayah'],
                        'pekerjaan_ibu' : req['pekerjaan_ibu'],
                        'no_telp_ayah' : req['no_telp_ayah'],
                        'no_telp_ibu' : req['no_telp_ibu']
                    }
                }

                update_student(filter, newVal)
                return {"success":True}
        else:
            return {"Success" : False, "msg" : "Only admin can perform this action"}
            

    #@jwt_required()
    def delete(self, student_id):
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            ObjInstance = ObjectId(student_id)
            filter = {'_id':ObjInstance}
            data = delete_student(filter)
            return {"success":True}
        else:
            return {"Success" : False, "msg" : "Only admin can perform this action"}

api.add_resource(Student, '/API/students/<student_id>')
