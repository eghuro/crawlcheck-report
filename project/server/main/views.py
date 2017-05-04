# project/server/main/views.py


#################
#### imports ####
#################

import queue
from flask import render_template, Blueprint, request
from sqlalchemy import text
from project.server import db
from project.server.models import Transaction, Link, Defect


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################


@main_blueprint.route('/')
def home():
    return render_template('main/home.html')


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")

@main_blueprint.route('/transaction')
def transactions():
    if 'ct' in request.args:
        if request.args['ct'] == "None":
            ct = None
        else:
            ct = request.args['ct']
    if 's' in request.args:
        if request.args['s'] == "None":
            s = None
        else:
            s = request.args['s']

    if 'ct' in request.args and 's' in request.args:
        t = Transaction.query.filter_by(status=s, ctype=ct).all()
    elif 'ct' in request.args:
        t = Transaction.query.filter_by(ctype=ct).all()
    elif 's' in request.args:
        t = Transaction.query.filter_by(status=s).all()
    else:
        t = Transaction.query.all()

    u = Transaction.query.all()
    status = set([x.status for x in u])
    ctype = set([x.ctype for x in u])

    return render_template('main/transaction.html', data=t, statuses=status, types=ctype)

@main_blueprint.route('/defect')
def defects():
    if 't' in request.args:
        d = Defect.query.filter_by(type=request.args['t']).all()
    else:
        d = Defect.query.all()
    y = Defect.query.all()
    types = set([x.type for x in y])
    return render_template('main/defect.html', defects=d, types=types)

@main_blueprint.route('/link')
def links():
    if 'p' in request.args:
        l = Link.query.filter_by(processed=request.args['p']).all()
    else:
        l = Link.query.all()
    return render_template('main/link.html', links=l)

@main_blueprint.route('/finding/<tid>')
def finding_detail(tid):
    t = Transaction.query.filter_by(id=tid).first()
    l = db.session.query(Link).from_statement(text("select * from link where responseId=:responseId or requestId=:requestId")).params(requestId=tid, responseId=tid).all()
    d = Defect.query.filter_by(responseId=tid).all()
    return render_template('main/finding_detail.html', transaction=t, links=l, defects=d)

@main_blueprint.route('/path/<tid>')
def transaction_path(tid):
    t0 = Transaction.query.filter_by(id=tid).first()
    transactions = [t0]
    tr = t0
    while tr.depth != 0:
        tr = Transaction.query.filter_by(id=tr.parentId).first()
        transactions.append(tr)
    return render_template('main/path.html', transaction=t0, transactions=transactions)
