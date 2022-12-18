import json
from bson.json_util import dumps
from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import *
from bson.objectid import ObjectId
from .db import insert_rapor, update_rapor, get_rapor, get_student

bp = Blueprint('rapor', __name__)
api = Api(bp)

class Rapor(Resource):
    @jwt_required()
    def get(self, student_id):
        ObjInstance = ObjectId(student_id)
        student = get_student({"_id":ObjInstance})
        rapor = get_rapor({"student_id"})
        return {"nama_peserta_didik":student["nama"],
        "rapor":json.loads(dumps(rapor))}

    


api.add_resource(Rapor, "/API/rapor/<student_id>")

class RaporDetail(Resource):
    @jwt_required()
    def put(self, rapor_id):
        ObjInstance = ObjectId(rapor_id)
        filter = {"_id":ObjInstance}
        req = request.form
        newvalues = {"$set":{
            "nilai" : 
            [   
                # PENILAIAN CEKLIS (dengan radio button)
                # NILAI MORAL DAN AGAMA (0)
                [
                    # NILAI AGAMA (0)
                    { 
                        'a' : req['0-0-a'],
                        'b' : req['0-0-b'],
                        'c' : req['0-0-c'],
                        'd' : req['0-0-d'],
                        'e' : req['0-0-e'],
                    },

                    # NILAI MORAL (1)
                    {
                        'a' : req['0-1-a'],
                        'b' : req['0-1-b'],
                        'c' : req['0-1-c'],
                    }
                ],

                # FISIK MOTORIK (1)
                [ 
                    # MOTORIK KASAR (0)
                    {
                        'a' : req['1-0-a'],
                        'b' : req['1-0-b'],
                        'c' : req['1-0-c'],
                        'd' : req['1-0-d'],
                    },

                    # MOTORIK HALUS (1)
                    {
                        'a' : req['1-1-a'],
                        'b' : req['1-1-b'],
                        'c' : req['1-1-c'],
                        'd' : req['1-1-d'],
                        'e' : req['1-1-e'],
                        'f' : req['1-1-f'],
                        'g': req['1-1-g'],
                    },

                    # KESEHATAN DAN PERILAKU KESELAMATAN (2)
                    {
                        'a' : req['1-2-a'],
                        'b' : req['1-2-b'],
                        'c' : req['1-2-c'],
                    }
                ],

                # BAHASA (2)
                [
                    # RESEPTIF (0)
                    {
                        'a' : req['2-0-a'],
                        'b' : req['2-0-b'],
                        'c' : req['2-0-c'],
                        'd' : req['2-0-d'],
                    },

                    # EKSPRESIF (1)
                    {
                        'a' : req['2-1-a'],
                        'b' : req['2-1-b'],
                        'c' : req['2-1-c'],
                        'd' : req['2-1-d'],
                        'e' : req['2-1-e'],
                        'f' : req['2-1-f'],
                        'g' : req['2-1-g'],
                    },

                    # LITERASI (2)
                    {
                        'a' : req['2-2-a'],
                        'b' : req['2-2-b'],
                        'c' : req['2-2-c'],
                        'd' : req['2-2-d'],
                        'e' : req['2-2-e'],
                        'f' : req['2-2-f'],
                    }
                ],

                # KOGNITIF (3)
                [
                    # BELAJAR DAN PEMECAHAN MASALAH (0)
                    {
                        'a' : req['3-0-a'],
                        'b' : req['3-0-b'],
                        'c' : req['3-0-c'],
                    },

                    # BERPIKIR LOGIS (1)
                    {
                        'a' : req['3-1-a'],
                        'b' : req['3-1-b'],
                        'c' : req['3-1-c'],
                        'd' : req['3-1-d'],
                        'e' : req['3-1-e'],
                        'f' : req['3-1-f'],
                    },

                    # BERPIKIR SIMBOLIK (MATEMATIKA SEDERHANA) (2)
                    {
                        'a' : req['3-2-a'],
                        'b' : req['3-2-b'],
                        'c' : req['3-2-c'],
                        'd' : req['3-2-d'],
                    }
                ],

                # SOSIAL EMOSIONAL (4)
                [
                    # KESADARAN DIRI (0)
                    {
                        'a' : req['4-0-a'],
                        'b' : req['4-0-b'],
                        'c' : req['4-0-c'],
                    },

                    # RASA TANGGUNG JAWAB KEPADA DIRI SENDIRI DAN ORANG LAIN (1)
                    {
                        'a' : req['4-1-a'],
                        'b' : req['4-1-b'],
                        'c' : req['4-1-c'],
                        'd' : req['4-1-d'],
                    },

                    #  PERILAKU PROSOSIAL (2)
                    {
                        'a' : req['4-2-a'],
                        'b' : req['4-2-b'],
                        'c' : req['4-2-c'],
                        'd' : req['4-2-d'],
                        'e' : req['4-2-e'],
                        'f' : req['4-2-f'],
                        'g' : req['4-2-g'],
                        'h' : req['4-2-h'],
                        'i' : req['4-2-i'],
                    }
                ],

                # SENI (5)
                [
                    # subpenilaian (0)
                    {
                        'a' : req['5-0-a'],
                        'b' : req['5-0-b'],
                        'c' : req['5-0-c'],
                        'd' : req['5-0-d'],
                        'e' : req['5-0-e'],
                        'f' : req['5-0-f'],
                    }
                ],

                # INFORMASI PERKEMBANGAN (dengan textarea) (6)
                [
                    # subpenilaian (0)
                    {
                        '1' : req['6-0-1'],
                        '2' : req['6-0-2'],
                        '3' : req['6-0-3'],
                        '4' : req['6-0-4'],
                        '5' : req['6-0-5'],
                        '6' : req['6-0-6'],
                    }
                ]
            ]
        }}

        update_rapor(filter,newvalues)
        return {"Success" : True, "msg" : "rapor successfully updated"}

api.add_resource(RaporDetail, "/API/rapor/detail/<rapor_id>")