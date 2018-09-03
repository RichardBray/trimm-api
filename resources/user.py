
from passlib.hash import pbkdf2_sha256
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
            self.json_response({'message': 'Looks like this user already exists :('}, 400)


class UserLogin(PageHandler):
    """
    Allows user to login
    """

    def post(self):
        data = json.loads(self.request.body)
        user_info = self._get_user_by_credentials(data)
        if user_info:
            _set_user_cookie(self, user_info['user_uuid']) 
            self.json_response({'message': 'user has successfully logged in'})
        else:
             _incorrect_credentials(self)

    def _get_user_by_credentials(self, data):
        """
        Checks if user email and password is correct
            :return: dict with user data from db
        """
        user_info = Users.select_where('user_email', data["email"])
        result = None
        if user_info:
            password_correct = pbkdf2_sha256.verify(
                data['password'], user_info[0]['user_password'])
            if password_correct:
              result = user_info[0]
        return result


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


class AuthenticateUser(PageHandler):
    """
    This method simply gets user data
    """
    @authorised_user
    def get(self, user_info=None):
        updated_user_info = self._remove_sensitive_info(user_info)
        self.json_response(json.dumps(updated_user_info))

    def _remove_sensitive_info(self, user_info):
        for field in ['user_password', 'user_id', 'user_uuid']:
            del user_info[field]
        return user_info


def _set_user_cookie(self, user_uuid):
    expires = datetime.utcnow() + timedelta(days=30)
    self.set_cookie('auth', user_uuid, expires=expires)

def _incorrect_credentials(self):
    self.json_response(
        {'message': 'Oops, looks like your username or password incorrect'}, 400)
