# project/server/main/views.py


#################
#### imports ####
#################

from flask import Blueprint, request
from project.server import db
from project.server.models import Transaction, Finding, Link, Defect, DefectType


################
#### config ####
################

rest_blueprint = Blueprint('rest', __name__,)


################
#### routes ####
################


@rest_blueprint.route('/data', methods = ['DELETE'])
def wipe():
    if request.method == 'DELETE':
        cnt = 0
        tables = [Transaction, Finding, Link, Defect, DefectType]
        for table in tables:
            records = table.query.all()
            for record in records:
                db.session.delete(record)
                cnt = cnt + 1
        db.session.commit()
        return "Wipe data: " + str(cnt)

@rest_blueprint.route('/data', methods = ['POST'])
def update():
    if request.method == 'POST':
        return "Update data"
