from tornado.web import RequestHandler
from passlib.hash import pbkdf2_sha256
import json


class UserRegister(RequestHandler):
    """
        https://passlib.readthedocs.io/en/stable/
    """
    def post(self):
        data = json.loads(self.request.body)
        hash = pbkdf2_sha256.hash(data['password'])
        print(hash)
        # get request body
        # # check if email address already exists
        # # if it does return an error if it doesn't continue
        # salt and hash the password
        # # put into database
        # return jwt token out of username and hashed password
        pass
