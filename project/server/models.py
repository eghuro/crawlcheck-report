# project/server/models.py


import datetime

from project.server import app, db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        )
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.email)


class Transaction(db.Model):

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(10), nullable=False)
    uri = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer)
    ctype = db.Column(db.String(255))
    verificationStatusId = db.Column(db.Integer)
    depth = db.Column(db.Integer, nullable=False)

    def __init__(self, id, method, uri, status, ctype, vsi, depth):
        self.id = id
        self.method = method
        self.uri = uri
        self.status = status
        self.ctype = ctype
        self.verificationStatusId = vsi
        self.depth = depth


class Link(db.Model):

    __tablename__ = "link"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    fromUri = db.Column(db.String(255), nullable=False)
    toUri = db.Column(db.String(255), nullable=False)
    processed = db.Column(db.Boolean, nullable=False)
    requestId = db.Column(db.Integer)
    responseId = db.Column(db.Integer, nullable=False)

    def __init__(self, id, fromUri, toUri, processed, requestId, responseId):
        self.id = id
        self.toUri = toUri
        self.fromUri = fromUri
        self.processed = processed
        self.requestId = requestId
        self.responseId = responseId


class Defect(db.Model):

    __tablename__ = "defect"

    findingId = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String)
    evidence = db.Column(db.String, nullable=False)
    severity = db.Column(db.Numeric, nullable=False)
    responseId = db.Column(db.Integer, nullable=False)
    uri = db.Column(db.String(255), nullable=False)

    def __init__(self, findingId, type, description, evidence, severity, responseId, uri):
        self.findingId = findingId
        self.type = type
        self.description = description
        self.evidence = evidence
        self.severity = severity
        self.responseId = responseId
        self.uri = uri

