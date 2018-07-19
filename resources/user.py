
from passlib.hash import pbkdf2_sha256
import uuid
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
            email_in_db = Users.query_single('user_email', data["email"])
            if not email_in_db:
                hashed_password = pbkdf2_sha256.hash(data['password'])
                user_data = {'email': data['email'], 'password': hashed_password}
                encoded_jwt = jwt.encode(
                    user_data, secret_key, algorithm='HS256').decode('utf-8')
                user_uuid = str(uuid.uuid4())
                test = (1, user_uuid, data['username'], data['email'], hashed_password)
                Users.insert_single(
                    'user_id, user_uuid, user_name, user_email, user_password', ', '.join(test))
                self.json_response(json.dumps({'token': encoded_jwt}))
            else:
                self.json_response({'message': 'this email already exists'})
        else:
            self.json_error()
