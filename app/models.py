# models.py

from datetime import datetime
from flask_login import UserMixin
from app import bcrypt
from app import db

user_bank_accounts = db.Table('user_bank_accounts',
                              db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                              db.Column('bank_account_id', db.Integer, db.ForeignKey('bank_account.id'),
                                        primary_key=True),
                              db.Column('created_at', db.DateTime, default=datetime.now),
                              db.Column('updated_at', db.DateTime, default=datetime.now, onupdate=datetime.now)
                              )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    country = db.Column(db.String(100))
    zipcode = db.Column(db.Integer)
    city = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    bank_accounts = db.relationship('BankAccount', secondary=user_bank_accounts,
                                    backref=db.backref('users', lazy=True))

    gender = db.Column(db.String(100))

    is_active = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(100))
    account_number = db.Column(db.Integer)
    account_type = db.Column(db.String(100))
    balance = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
