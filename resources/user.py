
from passlib.hash import pbkdf2_sha256
from tornado.options import define, options
from datetime import datetime, timedelta
import uuid
import json

# Project Imports
from resources.helpers import PageHandler, authorised_user
from resources.categories import default_categories
from models.mysql import Users


class UserRegister(PageHandler):
    """
        If data is in req body for registration `username, email, password`.
        Check if the email already exits in database.
        If email does not exist, add a new user to the db and return message
        with `auth` cookie.
    """
    def post(self):
        data = json.loads(self.request.body)
        email_in_db = Users.select_where('user_email', data["email"])
        if not email_in_db:
            hashed_password = pbkdf2_sha256.encrypt(data['password'])
            user_uuid = str(uuid.uuid4())
            default_currency = '£ - Pound Sterling'
            Users.insert_into(
                user_uuid=user_uuid,
                user_name=data['username'], 
                user_email=data['email'],
                user_currency=default_currency,
                user_password=hashed_password)
            
            _set_user_cookie(self, user_uuid)
            self.json_response(
                {'message': 'new user created and categories', 'currency': default_currency}, 201)
            default_categories(user_uuid)
        else:
            self.json_response({'message': 'this email already exists'}, 400)


class UserLogin(PageHandler):
    """
    Allows user to login
    """
    def post(self):
        data = json.loads(self.request.body)
        user_info = Users.select_where('user_email', data["email"])
        if user_info:
            password_correct = pbkdf2_sha256.verify(
                data['password'], user_info[0]['user_password'])
            if password_correct:
                _set_user_cookie(self, user_info[0]['user_uuid'])

                for field in ['user_password', 'user_id', 'user_uuid']:
                    del user_info[0][field]

                self.json_response(json.dumps(user_info[0]))
            else:
               _incorrect_credentials(self)
        else:
             _incorrect_credentials(self)


class UserEdit(PageHandler):
    """
    Edit user details
        :param user_info: dict
        :return: void
    """
    @authorised_user
    def put(self, user_info=None):
        data = json.loads(self.request.body)
        Users.update_where(
            'user_uuid', user_info['user_uuid'], user_currency=data['user_currency'])
        self.json_response(
            {'message': 'currency updated'})


class UserLogout(PageHandler):
    """
    Logs out user by removing `auth` cookie
    """
    def get(self):
        self.clear_cookie('auth')
        self.json_response(
            {'message': 'user has logged out'})


def _set_user_cookie(self, user_uuid):
    expires = datetime.utcnow() + timedelta(days=30)
    self.set_cookie('auth', user_uuid, expires=expires)

def _incorrect_credentials(self):
    self.json_response(
        {'message': 'username or password incorrect'}, 400)
