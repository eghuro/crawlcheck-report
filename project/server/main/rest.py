# project/server/main/views.py


#################
#### imports ####
#################

from flask import Blueprint, request
import yaml
import json
from project.server import db
from project.server.models import Transaction, Link, Defect, Alias
from sqlalchemy import select


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
        tables = [Transaction, Link, Defect, Alias]
        for table in tables:
            records = table.query.delete()
        db.session.commit()
        return "Wipe all data"

@rest_blueprint.route('/data', methods = ['POST'])
def update():
    if request.method == 'POST':
        cnt = 0
        data = yaml.safe_load(request.form['payload'])
        if 'transactions' in data:
            for record in data['transactions']:
                t = Transaction(record['id'], record['method'], record['uri'],
                                record['responseStatus'], record['contentType'],
                                record['verificationStatus'], record['depth'],
                                record['parentId'])
                cnt = cnt + 1
                db.session.add(t)
                for alias in record['aliases']:
                    a = Alias(record['id'], alias)
                    cnt = cnt + 1
                    db.session.add(a)

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

@rest_blueprint.route('/data', methods=['GET'])
def visual_export():
    data = dict()

    defects = Defect.query.all()

    dtc = 'defect-type-count'
    data[dtc] = dict()
    for d in defects:
        if d.type not in data[dtc]:
            data[dtc][d.type] = 0
        data[dtc][d.type] = data[dtc][d.type] + 1

    data['defect-type-count-array'] = [data[dtc][key] for key in data[dtc].keys()]
    data['defect-type-label-array'] = [key for key in data[dtc].keys()]

    data['severity-values'] = list(set([float(d.severity) for d in defects]))
    data['defect-type-severity'] = dict()
    for d in defects:
        data['defect-type-severity'][d.type]=float(d.severity)


    return json.dumps(data)

@rest_blueprint.route('/data/network', methods=['GET'])
def getNetJson():
    jsn = dict()

    t = Transaction.query.all()
    l = Link.query.all()

    jsn['type'] = 'NetworkGraph'
    jsn['label'] = 'Link network'
    jsn['protocol'] = 'OLSR'
    jsn['version'] = '0.6.6.2'
    jsn['metric'] = 'ETX'
    jsn['nodes'] = [ {"id" : x.id, "label" : x.uri } for x in t ]
    validIds = set([x.id for x in t])
    jsn['links'] = [ {"source" : x.requestId, "target" : x.responseId} for x in l if x.requestId in validIds and x.responseId in validIds]

    return json.dumps(jsn)
