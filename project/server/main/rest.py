# project/server/main/views.py


#################
#### imports ####
#################

from flask import Blueprint, request
import yaml
from project.server import db
from project.server.models import Transaction, Link, Defect


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
        tables = [Transaction, Link, Defect]
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
                t = Transaction(record['id'], record['method'], record['uri'],
                                record['responseStatus'], record['contentType'],
                                record['verificationStatusId'], record['depth'])
                cnt = cnt + 1
                db.session.add(t)
        if 'link' in data:
            for record in data['link']:
                processed = record['processed'].lower() == 'true'
                l = Link(record['findingId'], record['fromUri'], record['toUri'],
                         processed, record['requestId'], record['responseId'])

                cnt = cnt + 1
                db.session.add(l)
        if 'defect' in data:
            for record in data['defect']:
                d = Defect(record['findingId'], record['type'], record['description'],
                           record['evidence'], record['severity'], record['responseId'],
                           record['uri'])
                cnt = cnt + 1
                db.session.add(d)
        db.session.commit()
        return "Update data: " + str(cnt)
