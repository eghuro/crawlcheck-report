# project/server/main/views.py


#################
#### imports ####
#################

import queue
from flask import render_template, Blueprint, request
from sqlalchemy import text
from project.server import db
from project.server.models import Transaction, Link, Defect, Alias


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)
page_count = 30

types = set([x.type for x in Defect.query.all()])

u = Transaction.query.all()
status = set([x.status for x in u])
ctype = set([x.ctype for x in u])

################
#### routes ####
################


@main_blueprint.route('/')
def home():
    return render_template('main/home.html')


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")

@main_blueprint.route('/transaction/', defaults={'page' : 1})
@main_blueprint.route('/transaction/page/<int:page>')
def transactions(page):
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
        t = Transaction.query.filter_by(status=s, ctype=ct).paginate(page=page, per_page=page_count)
    elif 'ct' in request.args:
        t = Transaction.query.filter_by(ctype=ct).paginate(page=page, per_page=page_count)
    elif 's' in request.args:
        t = Transaction.query.filter_by(status=s).paginate(page=page, per_page=page_count)
    else:
        t = Transaction.query.paginate(page=page, per_page=page_count)

    return render_template('main/transaction.html', data=t, statuses=status, types=ctype)

@main_blueprint.route('/defect/', defaults={'page' : 1})
@main_blueprint.route('/defect/page/<int:page>')
def defects(page):
    if 't' in request.args:
        d = Defect.query.filter_by(type=request.args['t']).order_by(Defect.severity.desc()).paginate(page=page, per_page=page_count)
    else:
        d = Defect.query.order_by(Defect.severity.desc()).paginate(page=page, per_page=page_count)

    return render_template('main/defect.html', defects=d, types=types)

@main_blueprint.route('/defect/visual/')
def defects_visual():
    return render_template('main/defect_visual.html')

@main_blueprint.route('/link/', defaults={'page' : 1})
@main_blueprint.route('/link/page/<int:page>')
def links(page):
    if 'p' in request.args:
        l = Link.query.filter_by(processed=request.args['p']).paginate(page=page, per_page=page_count)
    else:
        l = Link.query.paginate(page=page, per_page=page_count)
    return render_template('main/link.html', links=l)

@main_blueprint.route('/finding/<tid>')
def finding_detail(tid):
    t = Transaction.query.filter_by(id=tid).first()
    a = Alias.query.filter_by(transactionId=tid).all()
    l = db.session.query(Link).from_statement(text("select * from link where responseId=:responseId or requestId=:requestId")).params(requestId=tid, responseId=tid).all()
    d = Defect.query.filter_by(responseId=tid).all()
    return render_template('main/finding_detail.html', transaction=t, aliases=a, links=l, defects=d)

@main_blueprint.route('/path/<tid>')
def transaction_path(tid):
    t0 = Transaction.query.filter_by(id=tid).first()
    transactions = [t0]
    tr = t0
    while tr.depth != 0:
        tr = Transaction.query.filter_by(id=tr.parentId).first()
        transactions.append(tr)
    return render_template('main/path.html', transaction=t0, transactions=transactions)
