# project/server/main/views.py


#################
#### imports ####
#################

from flask import Blueprint, request
import yaml
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
        cnt = 0
        data = yaml.safe_load(request.form['payload'])
        if 'transactions' in data:
            for record in data['transactions']:
                t = Transaction(record['id'], record['method'], record['responseStatus'],
                                record['contentType'], record['verificationStatusId'],
                                record['origin'], record['depth'])
                cnt = cnt + 1
                db.session.add(t)
        if 'finding' in data:
            for record in data['finding']:
                db.session.add(Finding(record['id'], record['responseId']))
        if 'link' in data:
            for record in data['link']:
                l = Link(record['findingId'], record['toUri'], record['processed'],
                         record['requestId'])
                cnt = cnt + 1
                db.session.add(l)
        if 'defectType' in data:
            for record in data['defectType']:
                dt = DefectType(record['id'], record['type'], record['description'])
                cnt = cnt + 1
                db.session.add(dt)
        if 'defect' in data:
            for record in data['defect']:
                d = Defect(record['findingId'], record['type'], record['evidence'],
                           record['severity'])
                cnt = cnt + 1
                db.session.add(d)
        db.session.commit()
        return "Update data: " + str(cnt)
