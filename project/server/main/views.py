# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint


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
    return render_template('main/transaction.html')

@main_blueprint.route('/finding')
def findings():
    return render_template('main/finding.html')

@main_blueprint.route('/finding/<tid>')
def finding_detail(tid):
    return render_template('main/finding_detail.html', transaction=tid)
