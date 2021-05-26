from flask import Blueprint
from flask_restful import Api, reqparse, Resource

fanfic_bp = Blueprint('fanfic_bp', __name__)
fanfic_api = Api(fanfic_bp)

from database.db import db
from database.models import AO3Table, AO3Schema
from sqlalchemy import and_, or_, not_

ao3_schema = AO3Schema()

from . import compute

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class FanficDatabase(Resource):
    def get(self, index):
        if index > compute.DB_SIZE - 1:
            return 400, 'index exceeds the current database size'

        similar_idxes = compute.index_KNN(index)
        rankings = {n + 1 : None for n in range(len(similar_idxes))}

        for n, other_index in enumerate(similar_idxes):
            similar_fic = db.session.get(AO3Table, other_index)
            rankings[n + 1] = ao3_schema.dump(similar_fic)

        main_fanfic = db.session.get(AO3Table, index)

        return {
            'main': ao3_schema.dump(main_fanfic),
            'similar': rankings
        }


parser = reqparse.RequestParser(bundle_errors=True)

parser.add_argument('user_input', type=str, default='', location='form')

parser.add_argument('fandom', type=str, default='', location='form')

parser.add_argument('characters', type=str, default='', location='form')
parser.add_argument('relationships', type=str, default='', location='form')
parser.add_argument('tags', type=str, default='', location='form')


class FanficQuery(Resource):
    def get(self):
        args = parser.parse_args()

        # sanity check
        if not (args.user_input or args.fandom or args.characters or args.relationships or args.tags):
            return {'message': 'no argument'}, 400 

        if args.user_input != '':
            similar_idxes = compute.input_KNN(args.user_input)

            rankings = {n + 1 : None for n in range(len(similar_idxes))}

            for n, other_index in enumerate(similar_idxes):
                similar_fic = db.session.get(AO3Table, other_index)
                rankings[n + 1] = ao3_schema.dump(similar_fic)
            
            return rankings, 200

        elif args.fandom != '':
            ao3_fandom_names = compute.fandom_KNN(args.fandom)
            if not ao3_fandom_names:
                return {'message': 'fandom does not exist'}, 400 

            rankings = []
            conds = tuple([AO3Table.fandoms.contains(f) for f in ao3_fandom_names])

            results = db.session.query(AO3Table).filter(
                or_(*conds)
            ).order_by(AO3Table.kudos.desc())

            for row in results:
                rankings.append(ao3_schema.dump(row))
                if len(rankings) >= 500:
                    break

            return {n + 1: fanfic for n, fanfic in enumerate(rankings)}, 200

        else:
            chars, rls, tags = args.characters, args.relationships, args.tags
            queries = (chars, rls, tags)
            similar_idxes = compute.query_KNN(queries)

            rankings = {n + 1 : None for n in range(len(similar_idxes))}

            for n, other_index in enumerate(similar_idxes):
                similar_fic = db.session.get(AO3Table, other_index)
                rankings[n + 1] = ao3_schema.dump(similar_fic)
            
            return rankings, 200


class FanficMeta(Resource):
    def get(self, cat):
        if cat == 'characters':
            pass
        elif cat == 'fandoms':
            pass
        else:
            return {
                'message': 'meta type not supported'
            }, 400


fanfic_api.add_resource(FanficDatabase, '/fanfic/<int:index>')
fanfic_api.add_resource(FanficQuery, '/query')
fanfic_api.add_resource(FanficMeta, '/meta/<string:cat>')

