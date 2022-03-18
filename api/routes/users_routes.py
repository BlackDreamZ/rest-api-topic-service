# -*- encoding: utf-8 -*-

from datetime import datetime, timezone, timedelta

from functools import wraps

from flask import request
from flask_restx import Namespace,Api, Resource, fields

import jwt

from api.models.users_model import db, Users, JWTTokenBlocklist
#from api.models.category_model import CategorysProduct
from api.config import BaseConfig

def init_route_users(app, rest_api):
    signup_model = rest_api.model('SignUpModel', {"username": fields.String(required=True, min_length=2, max_length=32),
                                                  "email": fields.String(required=True, min_length=4, max_length=64),
                                                  "password": fields.String(required=True, min_length=4, max_length=16)
                                                  })

    signup_tg_model = rest_api.model('SignUpTelegramModel',
                                     {"username": fields.String(required=False, min_length=2, max_length=32),
                                      "id_tg": fields.Integer(required=False, min_length=4, max_length=100)
                                      })

    get_balance_user_tg_model = rest_api.model('GetBalanceUserModel',
                                               {"id_tg": fields.Integer(required=True, min_length=4, max_length=100)})

    update_balance_user_tg_model = rest_api.model('UpdateBalanceUserModel',
                                                  {"id_tg": fields.Integer(required=True, min_length=4, max_length=100),
                                                   "value": fields.Float(required=True, min_length=4, max_length=100)})

    login_model = rest_api.model('LoginModel', {"email": fields.String(required=True, min_length=4, max_length=64),
                                                "password": fields.String(required=True, min_length=4, max_length=16)
                                                })

    user_edit_model = rest_api.model('UserEditModel', {"id_tg": fields.String(required=True, min_length=1, max_length=100),
                                                       "username": fields.String(required=False, min_length=2,
                                                                                 max_length=32),
                                                       "email": fields.String(required=False, min_length=4, max_length=64)
                                                       })

    # get_all_category = rest_api.model('GetAllCategory')

    """
       Helper function for JWT token required
    """


    def token_required(f):
        @wraps(f)
        def decorator(*args, **kwargs):

            token = None

            if "authorization" in request.headers:
                token = request.headers["authorization"]

            if not token:
                return {"success": False, "msg": "Valid JWT token is missing"}, 400

            try:
                data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=["HS256"])
                current_user = Users.get_by_email(data["email"])

                if not current_user:
                    return {"success": False,
                            "msg": "Sorry. Wrong auth token. This user does not exist."}, 400

                token_expired = db.session.query(JWTTokenBlocklist.id).filter_by(jwt_token=token).scalar()

                if token_expired is not None:
                    return {"success": False, "msg": "Token revoked."}, 400

                if not current_user.check_jwt_auth_active():
                    return {"success": False, "msg": "Token expired."}, 400

            except:
                return {"success": False, "msg": "Token is invalid"}, 400

            return f(current_user, *args, **kwargs)

        return decorator


    """
        Flask-Restx routes
    """


    @rest_api.route('/api/users/register')
    class Register(Resource):
        """
           Creates a new user by taking 'signup_model' input
        """

        @rest_api.expect(signup_model, validate=True)
        def post(self):
            req_data = request.get_json()

            _username = req_data.get("username")
            _email = req_data.get("email")
            _password = req_data.get("password")

            user_exists = Users.get_by_email(_email)
            if user_exists:
                return {"success": False,
                        "msg": "Email already taken"}, 400

            new_user = Users(username=_username, email=_email)

            new_user.set_password(_password)
            new_user.save()

            return {"success": True,
                    "userID": new_user.id,
                    "msg": "The user was successfully registered"}, 200


    @rest_api.route('/api/users/register_tg')
    class Registertg(Resource):
        """
           Creates a new user by taking 'signup_model_tg' input
        """

        @rest_api.expect(signup_tg_model, validate=True)
        def post(self):
            req_data = request.get_json()
            _username = req_data.get("username")
            _id_tg = req_data.get("id_tg")
            user_exists = Users.get_by_id_tg(_id_tg)
            if user_exists:
                return {"success": False,
                        "msg": "Telegram id already taken"}, 400

            new_user = Users(username=_username, id_tg=_id_tg)
            new_user.save()

            return {"success": True,
                    "userID": new_user.id,
                    "msg": "The user was successfully registered"}


    @rest_api.route('/api/users/get_balance', doc={"description": "Метод для получения баланса пользователя"})
    @rest_api.response(404, 'Telegram id is not found')
    @rest_api.response(200, 'Successful receipt balance ')
    @rest_api.param('id_tg', 'The telegram user identifier')
    class GetBalance(Resource):
        """
          Get balance user tg 'get_balance'
        """

        @rest_api.expect(get_balance_user_tg_model, validate=True)
        def post(self):
            req_data = request.get_json()
            _id_tg = req_data.get("id_tg")
            user_balance = Users.get_balance_by_id_tg(_id_tg)
            if not user_balance:
                return {"success": False,
                        "msg": "Telegram id is not found"}, 404

            return {
                       "success": True,
                       "balance": user_balance.balance
                   }, 200


    @rest_api.route('/api/users/update_balance')
    class UpdateBalance(Resource):
        """
          Get balance user tg 'update_balance'
        """

        @rest_api.expect(update_balance_user_tg_model, validate=True)
        def post(self):
            req_data = request.get_json()

            _id_tg = req_data.get("id_tg")
            _value = req_data.get("value")

            user = Users.get_balance_by_id_tg(_id_tg)
            if not user:
                return {"success": False,
                        "msg": "Telegram id is not found"}, 400

            user.update_balance(_value)
            user.save()

            return {
                       "success": True,
                       "balance": user.balance
                   }, 200


    @rest_api.route('/api/users/login')
    class Login(Resource):
        """
           Login user by taking 'login_model' input and return JWT token
        """

        @rest_api.expect(login_model, validate=True)
        def post(self):

            req_data = request.get_json()

            _email = req_data.get("email")
            _password = req_data.get("password")

            user_exists = Users.get_by_email(_email)

            if not user_exists:
                return {"success": False,
                        "msg": "This email does not exist."}, 400

            if not user_exists.check_password(_password):
                return {"success": False,
                        "msg": "Wrong credentials."}, 400

            # create access token uwing JWT
            token = jwt.encode({'email': _email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, BaseConfig.SECRET_KEY)

            user_exists.set_jwt_auth_active(True)
            user_exists.save()

            return {"success": True,
                    "token": token,
                    "user": user_exists.toJSON()}, 200


    @rest_api.route('/api/users/edit')
    class EditUser(Resource):
        """
           Edits User's username or password or both using 'user_edit_model' input
        """

        @rest_api.expect(user_edit_model)
        # @token_required
        def post(self):

            req_data = request.get_json()

            _new_username = req_data.get("username")
            _new_email = req_data.get("email")
            _id_tg = req_data.get("id_tg")

            user_exists = Users.get_by_id_tg(_id_tg)
            if not user_exists:
                return {"success": False,
                        "msg": "This email does not exist."}, 400
            if _new_username:
                user_exists.update_username(_new_username)

            if _new_email:
                user_exists.update_email(_new_email)

            user_exists.save()

            return {"success": True}, 200


    @rest_api.route('/api/users/logout')
    class LogoutUser(Resource):
        """
           Logs out User using 'logout_model' input
        """

        @token_required
        def post(self, current_user):
            _jwt_token = request.headers["authorization"]

            jwt_block = JWTTokenBlocklist(jwt_token=_jwt_token, created_at=datetime.now(timezone.utc))
            jwt_block.save()

            self.set_jwt_auth_active(False)
            self.save()

            return {"success": True}, 200





