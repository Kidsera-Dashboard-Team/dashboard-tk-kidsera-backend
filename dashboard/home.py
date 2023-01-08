from flask import Blueprint,current_app,request,jsonify
from.db import get_info, getAll_student
from bson.json_util import dumps
from flask_restful import Api, Resource
from hashlib import md5
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import datetime
import json

bp = Blueprint("home",__name__)
api = Api(bp)

class Home(Resource):
    @jwt_required()
    def get(self):
        info = get_info()
        siswaLaki = len(list(getAll_student({"jenis_kelamin":"Laki-laki","tahun_ajaran":"2022/2023"})))
        siswaPerempuan = len(list(getAll_student({"jenis_kelamin":"Perempuan","tahun_ajaran":"2022/2023"})))
        siswaA = len(list(getAll_student({"tingkat_kelas":"A","tahun_ajaran":"2022/2023"})))
        siswaB = len(list(getAll_student({"tingkat_kelas":"B","tahun_ajaran":"2022/2023"})))
        return {"siswa_laki":siswaLaki,
        "siswa_perempuan":siswaPerempuan, 
        "siswa_A":siswaA,
        "siswa_B":siswaB,
        "info":json.loads(dumps(info))}

api.add_resource(Home,"/API/")
