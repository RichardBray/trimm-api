
from passlib.hash import pbkdf2_sha256
import json
import jwt

# Project Imports
from resources.helpers import PageHandler
from models.mysql import Users

# TODO Generate better secret key
secret_key = "secret"


class UserRegister(PageHandler):
    """
        https://passlib.readthedocs.io/en/stable/
        https://pyjwt.readthedocs.io/en/latest/
    """
    def post(self):
        if self.request.body:
            data = json.loads(self.request.body)
            '''
                TODO figure out uuid for db
            '''
            email_in_db = Users.query_single('email', data['email'])
            if email_in_db:
                hash_password = pbkdf2_sha256.hash(data['password'])
                user_data = {'email': data['email'], 'password': hash_password}
                encoded_jwt = jwt.encode(
                    user_data, secret_key, algorithm='HS256').decode('utf-8')
                self.json_response(json.dumps({'token': encoded_jwt}))
            else:
                self.json_response({'message': 'this email already exists'})
        else:
            self.json_error()
