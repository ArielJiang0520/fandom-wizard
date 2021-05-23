from flask import Blueprint, request
from database.db import db
from database.models import AO3, AO3Schema

ao3 = Blueprint('ao3', __name__)
ao3_schema = AO3Schema()

from . import dataloader
import os

curr_file_path = os.path.dirname(os.path.realpath(__file__))
E = dataloader.load_matrix(os.path.join(curr_file_path, 'matrix'))

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
    if 'index' in request.args:
        index = int(request.args['index'])
        idxes = compute.KNN(E, index, 50)
        result = db.session.query(AO3).filter(AO3.index.in_(idxes))

        rankings = {n: None for n in range(50)}
        for n, row in enumerate(result):
            rankings[n] = ao3_schema.dump(row)
        return rankings
    return {}