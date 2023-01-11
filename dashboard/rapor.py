import json
from bson.json_util import dumps
from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import *
from bson.objectid import ObjectId

from .db import insert_rapor, update_rapor, get_rapor, get_student, get_user, delete_rapor

bp = Blueprint('rapor', __name__)
api = Api(bp)

class Rapor(Resource):
    #@jwt_required()
    def post(self, student_id):
        req = request.get_json()
        id = ObjectId(student_id)
        student = get_student(id)
        periode = req['periode']

        if periode == "tengah_semester":
            data = {
                "student_id" : id,
                "tahun_ajaran" : student['tahun_ajaran'],
                "periode" : req['periode'],
                "semester" : req['semester'],
                "nilai" : 
                  [
                    # subpenilaian 
                    [
                        {
                            'text1' : req['text1'],
                            'text2' : req['text2'],
                            'text3' : req['text3'],
                            'text4' : req['text4'],
                            'text5' : req['text5'],
                            'text6' : req['text6'],
                        }
                    ]
                ]
            }    
        else:
            data = {
                "student_id" : id,
                "tahun_ajaran" : student['tahun_ajaran'],
                "periode" : req['periode'],
                "semester" : req['semester'],
                
                "nilai" : 
                [   
                    # PENILAIAN CEKLIS (dengan radio button)
                    # NILAI MORAL DAN AGAMA (a)
                    [
                        # NILAI AGAMA (a)
                        { 
                            'a' : req['aaa'],
                            'b' : req['aab'],
                            'c' : req['aac'],
                            'd' : req['aad'],
                            'e' : req['aae'],
                        },

                        # NILAI MORAL (b)
                        {
                            'a' : req['aba'],
                            'b' : req['abb'],
                            'c' : req['abc'],
                        }
                    ],

                    # FISIK MOTORIK (b)
                    [ 
                        # MOTORIK KASAR (a)
                        {
                            'a' : req['baa'],
                            'b' : req['bab'],
                            'c' : req['bac'],
                            'd' : req['bad'],
                        },

                        # MOTORIK HALUS (b)
                        {
                            'a' : req['bba'],
                            'b' : req['bbb'],
                            'c' : req['bbc'],
                            'd' : req['bbd'],
                            'e' : req['bbe'],
                            'f' : req['bbf'],
                            'g' : req['bbg'],
                        },

                        # KESEHATAN DAN PERILAKU KESELAMATAN (c)
                        {
                            'a' : req['bca'],
                            'b' : req['bcb'],
                            'c' : req['bcc'],
                        }
                    ],

                    # BAHASA (c)
                    [
                        # RESEPTIF (a)
                        {
                            'a' : req['caa'],
                            'b' : req['cab'],
                            'c' : req['cac'],
                            'd' : req['cad'],
                        },

                        # EKSPRESIF (b)
                        {
                            'a' : req['cba'],
                            'b' : req['cbb'],
                            'c' : req['cbc'],
                            'd' : req['cbd'],
                            'e' : req['cbe'],
                            'f' : req['cbf'],
                            'g' : req['cbg'],
                        },

                        # LITERASI (c)
                        {
                            'a' : req['cca'],
                            'b' : req['ccb'],
                            'c' : req['ccc'],
                            'd' : req['ccd'],
                            'e' : req['cce'],
                            'f' : req['ccf'],
                        }
                    ],

                    # KOGNITIF (3)
                    [
                        # BELAJAR DAN PEMECAHAN MASALAH (a)
                        {
                            'a' : req['daa'],
                            'b' : req['dab'],
                            'c' : req['dac'],
                        },

                        # BERPIKIR LOGIS (b)
                        {
                            'a' : req['dba'],
                            'b' : req['dbb'],
                            'c' : req['dbc'],
                            'd' : req['dbd'],
                            'e' : req['dbe'],
                            'f' : req['dbf'],
                        },

                        # BERPIKIR SIMBOLIK (MATEMATIKA SEDERHANA) (c)
                        {
                            'a' : req['dca'],
                            'b' : req['dcb'],
                            'c' : req['dcc'],
                            'd' : req['dcd'],
                        }
                    ],

                    # SOSIAL EMOSIONAL (e)
                    [
                        # KESADARAN DIRI (a)
                        {
                            'a' : req['eaa'],
                            'b' : req['eab'],
                            'c' : req['eac'],
                        },

                        # RASA TANGGUNG JAWAB KEPADA DIRI SENDIRI DAN ORANG LAIN (b)
                        {
                            'a' : req['eba'],
                            'b' : req['ebb'],
                            'c' : req['ebc'],
                            'd' : req['ebd'],
                        },

                        #  PERILAKU PROSOSIAL (c)
                        {
                            'a' : req['eca'],
                            'b' : req['ecb'],
                            'c' : req['ecc'],
                            'd' : req['ecd'],
                            'e' : req['ece'],
                            'f' : req['ecf'],
                            'g' : req['ecg'],
                            'h' : req['ech'],
                            'i' : req['eci'],
                        }
                    ],

                    # SENI (f)
                    [
                        # subpenilaian (a)
                        {
                            'a' : req['faa'],
                            'b' : req['fab'],
                            'c' : req['fac'],
                            'd' : req['fad'],
                            'e' : req['fae'],
                            'f' : req['faf'],
                        }
                    ],

                    # INFORMASI PERKEMBANGAN (dengan textarea) (g)
                    [
                        # subpenilaian (a)
                        {
                            'text1' : req['text1'],
                            'text2' : req['text2'],
                            'text3' : req['text3'],
                            'text4' : req['text4'],
                            'text5' : req['text5'],
                            'text6' : req['text6'],
                        }
                    ]
                ]
            }

        insert_rapor(data)
        return {"Success" : True, "msg" : "rapor successfully added", "inserted_data" : json.loads(dumps(data))}

    #@jwt_required()
    def get(self, student_id):
        ObjInstance = ObjectId(student_id)
        student = get_student({"_id":ObjInstance})
        rapor = get_rapor({"student_id":ObjInstance})
        data =  {"nama_peserta_didik":student, "rapor":json.loads(dumps(rapor))}
        return json.loads(dumps(data)) 


api.add_resource(Rapor, "/API/rapor/<student_id>")

class RaporDetail(Resource):
    def get(self, student_id, periode, semester ):
        ObjInstance = ObjectId(student_id)
        student = get_student({"_id":ObjInstance})
        rapor = get_rapor({"student_id":ObjInstance, "periode":periode, "semester":semester})
        data =  {"nama_peserta_didik":student, "rapor":json.loads(dumps(rapor))}
        return json.loads(dumps(data)) 

    #@jwt_required()
    def put(self, student_id, periode, semester):
        ObjInstance = ObjectId(student_id)
        filter = {"student_id":ObjInstance, "periode":periode, "semester":semester}
        req = request.get_json()

        if periode == "tengah_semester":
            newvalues = {"$set":{
                "nilai" : 
                    [    [
                            {
                                'text1' : req['text1'],
                                'text2' : req['text2'],
                                'text3' : req['text3'],
                                'text4' : req['text4'],
                                'text5' : req['text5'],
                                'text6' : req['text6'],
                            }
                        ]
                    ]
                }
            }
        else:
            newvalues = {"$set":{
                "nilai" : 
                    [   
                        # PENILAIAN CEKLIS (dengan radio button)
                        # NILAI MORAL DAN AGAMA (a)
                        [
                            # NILAI AGAMA (a)
                            { 
                                'a' : req['aaa'],
                                'b' : req['aab'],
                                'c' : req['aac'],
                                'd' : req['aad'],
                                'e' : req['aae'],
                            },

                            # NILAI MORAL (b)
                            {
                                'a' : req['aba'],
                                'b' : req['abb'],
                                'c' : req['abc'],
                            }
                        ],

                        # FISIK MOTORIK (b)
                        [ 
                            # MOTORIK KASAR (a)
                            {
                                'a' : req['baa'],
                                'b' : req['bab'],
                                'c' : req['bac'],
                                'd' : req['bad'],
                            },

                            # MOTORIK HALUS (b)
                            {
                                'a' : req['bba'],
                                'b' : req['bbb'],
                                'c' : req['bbc'],
                                'd' : req['bbd'],
                                'e' : req['bbe'],
                                'f' : req['bbf'],
                                'g' : req['bbg'],
                            },

                            # KESEHATAN DAN PERILAKU KESELAMATAN (c)
                            {
                                'a' : req['bca'],
                                'b' : req['bcb'],
                                'c' : req['bcc'],
                            }
                        ],

                        # BAHASA (c)
                        [
                            # RESEPTIF (a)
                            {
                                'a' : req['caa'],
                                'b' : req['cab'],
                                'c' : req['cac'],
                                'd' : req['cad'],
                            },

                            # EKSPRESIF (b)
                            {
                                'a' : req['cba'],
                                'b' : req['cbb'],
                                'c' : req['cbc'],
                                'd' : req['cbd'],
                                'e' : req['cbe'],
                                'f' : req['cbf'],
                                'g' : req['cbg'],
                            },

                            # LITERASI (c)
                            {
                                'a' : req['cca'],
                                'b' : req['ccb'],
                                'c' : req['ccc'],
                                'd' : req['ccd'],
                                'e' : req['cce'],
                                'f' : req['ccf'],
                            }
                        ],

                        # KOGNITIF (3)
                        [
                            # BELAJAR DAN PEMECAHAN MASALAH (a)
                            {
                                'a' : req['daa'],
                                'b' : req['dab'],
                                'c' : req['dac'],
                            },

                            # BERPIKIR LOGIS (b)
                            {
                                'a' : req['dba'],
                                'b' : req['dbb'],
                                'c' : req['dbc'],
                                'd' : req['dbd'],
                                'e' : req['dbe'],
                                'f' : req['dbf'],
                            },

                            # BERPIKIR SIMBOLIK (MATEMATIKA SEDERHANA) (c)
                            {
                                'a' : req['dca'],
                                'b' : req['dcb'],
                                'c' : req['dcc'],
                                'd' : req['dcd'],
                            }
                        ],

                        # SOSIAL EMOSIONAL (e)
                        [
                            # KESADARAN DIRI (a)
                            {
                                'a' : req['eaa'],
                                'b' : req['eab'],
                                'c' : req['eac'],
                            },

                            # RASA TANGGUNG JAWAB KEPADA DIRI SENDIRI DAN ORANG LAIN (b)
                            {
                                'a' : req['eba'],
                                'b' : req['ebb'],
                                'c' : req['ebc'],
                                'd' : req['ebd'],
                            },

                            #  PERILAKU PROSOSIAL (c)
                            {
                                'a' : req['eca'],
                                'b' : req['ecb'],
                                'c' : req['ecc'],
                                'd' : req['ecd'],
                                'e' : req['ece'],
                                'f' : req['ecf'],
                                'g' : req['ecg'],
                                'h' : req['ech'],
                                'i' : req['eci'],
                            }
                        ],

                        # SENI (f)
                        [
                            # subpenilaian (a)
                            {
                                'a' : req['faa'],
                                'b' : req['fab'],
                                'c' : req['fac'],
                                'd' : req['fad'],
                                'e' : req['fae'],
                                'f' : req['faf'],
                            }
                        ],

                        # INFORMASI PERKEMBANGAN (dengan textarea) (g)
                        [
                            # subpenilaian (a)
                            {
                                'text1' : req['text1'],
                                'text2' : req['text2'],
                                'text3' : req['text3'],
                                'text4' : req['text4'],
                                'text5' : req['text5'],
                                'text6' : req['text6'],
                            }
                        ]
                    ]
            }
        }

        update_rapor(filter,newvalues)
        return {"Success" : True, "msg" : "rapor successfully updated"}


    #@jwt_required()
    def delete(self, student_id, periode, semester):
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            ObjInstance = ObjectId(student_id)
            filter = {"student_id":ObjInstance, "periode":periode, "semester":semester}
            delete_rapor(filter)
            print(filter)
            return{"success":True}
        else:
            return{"success":False, "msg":"only admin can perform this action"}

api.add_resource(RaporDetail, "/API/rapor/detail/<student_id>/<periode>/<semester>")
