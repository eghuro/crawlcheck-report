# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint
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
    t = Transaction.query.all()
    return render_template('main/transaction.html', data=t) #TODO: statuses, content-types

@main_blueprint.route('/finding')
def findings():
    l = Link.query.all()
    d = Defect.query.all()
    return render_template('main/finding.html', links=l, defects=d)

@main_blueprint.route('/finding/<tid>')
def finding_detail(tid):
    t = Transaction.query.filter_by(id=tid).first()
    l = Link.query.filter_by(response_id=tid).all()
    d = Defect.query.filter_by(response_id=tid).all()
    return render_template('main/finding_detail.html', transaction=t, links=l, defects=d)
