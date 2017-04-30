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


class Finding(db.Model):

    __tablename__ = "finding"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    responseId = db.Column(db.Integer, nullable=False)


class Link(db.Model):

    __tablename__ = "link"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    toUri = db.Column(db.String(255), nullable=False)
    processed = db.Column(db.Boolean, nullable=False)
    requestId = db.Column(db.Integer)


class DefectType(db.Model):

    __tablename__ = "defectType"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String)


class Defect(db.Model):

    __tablename__ = "defect"

    findingId = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    evidence = db.Column(db.String, nullable=False)
    severity = db.Column(db.Numeric, nullable=False)
