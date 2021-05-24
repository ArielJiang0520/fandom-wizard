from flask import Blueprint, request
ao3 = Blueprint('ao3', __name__)

from database.db import db
from database.models import AO3, AO3Schema, VECTOR
ao3_schema = AO3Schema()

from database.vectors import read_embed_matrix
E, T, C = read_embed_matrix(db, VECTOR, hard_refresh=False) # Turn this to true if you just pulled it

from . import compute

@ao3.route('/fanfic', methods=['GET'])
def fanfic():
    if 'index' in request.args:
        index = int(request.args['index'])
        result = db.session.get(AO3, index)
        return ao3_schema.dump(result)
    return {}

@ao3.route('/fanfic/sim', methods=['GET'])
def fanfic_sim():
    idxes = []

    if 'index' in request.args:
        index = int(request.args['index'])
        idxes = compute.index_KNN(E, index, 50)
    
    elif 'input' in request.args:
        input = request.args['input']
        idxes = compute.input_KNN(E, input, 50)

    if idxes:
        result = db.session.query(AO3).filter(AO3.index.in_(idxes))

        rankings = {n: None for n in range(50)}
        for n, row in enumerate(result):
            rankings[n] = ao3_schema.dump(row)
        return rankings
    
    return {}

