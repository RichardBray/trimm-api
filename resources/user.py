
from passlib.hash import pbkdf2_sha256
from tornado.options import define, options
import uuid
import json
import jwt

# Project Imports
from resources.helpers import PageHandler
from models.mysql import Users

# TODO Generate better secret key

define('secret_key', default='')
secret_key = options.secret_key


class UserRegister(PageHandler):
    """
        Creates a user and adds their information to the database
    """
    def post(self):
        if self.request.body:
            data = json.loads(self.request.body)
            email_in_db = Users.query_single('user_email', data["email"])
            if not email_in_db:
                hashed_password = pbkdf2_sha256.hash(data['password'])
                Users.insert_single(
                    user_uuid=str(uuid.uuid4()), 
                    user_name=data['username'], 
                    user_email=data['email'], 
                    user_password=hashed_password)

                user_token_data = {'email': data['email'], 'password': hashed_password}
                encoded_jwt = jwt.encode(
                    user_token_data, secret_key, algorithm='HS256').decode('utf-8')                    
                self.json_response(json.dumps({'token': encoded_jwt}))
            else:
                self.json_response({'message': 'this email already exists'})
        else:
            self.json_error()
