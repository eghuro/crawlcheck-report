# project/server/main/views.py


#################
#### imports ####
#################

from flask import Blueprint, request


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
        return "Wipe data"

@rest_blueprint.route('/data', methods = ['POST'])
def update():
    if request.method == 'POST':
        return "Update data"
