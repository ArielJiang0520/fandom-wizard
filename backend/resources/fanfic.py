from flask import Blueprint, request
from flask_restful import Api, fields, marshal_with, reqparse, Resource
from transformers.utils.dummy_pt_objects import default_data_collator
from flask_restplus import abort

fanfic_bp = Blueprint('fanfic_bp', __name__)
fanfic_api = Api(fanfic_bp)

from database.db import db
from database.models import AO3Table, AO3Schema, MatrixTable

ao3_schema = AO3Schema()

from database.vectors import read_embed_matrix

E, T, C, S = read_embed_matrix(db, MatrixTable, hard_refresh=False) # Turn this to true if you just pulled it

from . import compute

class FanficDatabase(Resource):
    def get(self, index):
        curr_db_size = E.shape[0]
        if index > curr_db_size - 1:
            abort(400, 'index exceeds the current database size')

        similar_idxes = compute.index_KNN((E, T, C, S), index, 50)
        rankings = {n + 1 : None for n in range(50)}

        for n, other_index in enumerate(similar_idxes):
            similar_fic = db.session.get(AO3Table, other_index)
            rankings[n + 1] = ao3_schema.dump(similar_fic)

        main_fanfic = db.session.get(AO3Table, index)

        return {
            'main': ao3_schema.dump(main_fanfic),
            'similar': rankings
        }

parser = reqparse.RequestParser()
parser.add_argument('use_text', required=True, type=bool, location='form')
parser.add_argument('user_input', type=str, default='', location='form')
parser.add_argument('characters', type=str, default='', location='form')

class FanficQuery(Resource):
    def get(self):
        args = parser.parse_args()
        
        if args.use_text:
            if args.user_input == '':
                abort(400, custom='user input can not be empty, switch to use_text=False instead')

            similar_idxes = compute.input_KNN((E, S), args.user_input, 50)
            rankings = {n + 1 : None for n in range(50)}

            for n, other_index in enumerate(similar_idxes):
                similar_fic = db.session.get(AO3Table, other_index)
                rankings[n + 1] = ao3_schema.dump(similar_fic)
            
            return rankings, 200

        else:
            return {}, 204

fanfic_api.add_resource(FanficDatabase, '/fanfic/<int:index>')
fanfic_api.add_resource(FanficQuery, '/query')
