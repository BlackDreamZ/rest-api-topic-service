# -*- encoding: utf-8 -*-

from datetime import datetime

import json

from werkzeug.security import generate_password_hash, check_password_hash

from api.models import db

# Таблица пользователи
class Users(db.Model):
    # Поля таблицы
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64) )
    id_tg = db.Column(db.Integer())
    password = db.Column(db.Text())
    jwt_auth_active = db.Column(db.Boolean())
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)
    balance = db.Column(db.Float(),default=0)
    def __repr__(self):
        return "User {self.username}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_email(self, new_email):
        self.email = new_email

    def update_username(self, id_telegram):
        self.id_telegram = id_telegram

    def update_username(self, new_username):
        self.username = new_username

    def update_balance(self, balance):
        self.balance += balance

    def check_jwt_auth_active(self):
        return self.jwt_auth_active

    def set_jwt_auth_active(self, set_status):
        self.jwt_auth_active = set_status

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_id(cls, id_tg):
        return cls.query.filter_by(id_tg=id_tg).first()


    @classmethod
    def get_by_id_tg(cls, id_tg):
        return cls.query.filter_by(id_tg=id_tg).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_balance_by_id_tg(cls, id_tg):
        return cls.query.filter_by(id_tg=id_tg).first()

    def toDICT(self):

        cls_dict = {}
        cls_dict['_id'] = self.id
        cls_dict['username'] = self.username
        cls_dict['email'] = self.email

        return cls_dict

    def toJSON(self):

        return self.toDICT()


class JWTTokenBlocklist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jwt_token = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return "Expired Token: {self.jwt_token}"

    def save(self):
        db.session.add(self)
        db.session.commit()


