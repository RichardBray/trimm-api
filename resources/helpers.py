from tornado.web import RequestHandler
from models.mysql import Users
import json
from tornado.options import options
import sys


def _get_env(arg=None):
    """
    Returns environment variable from command line
    """
    if arg:
        split_arg = arg.split('=')
        return split_arg[1]


class PageHandler(RequestHandler):
    api_url = "http://app.trimm.me"

    if len(sys.argv) > 1:
        env = _get_env(sys.argv[1])
        if env == "dev":
            api_url = "http://localhost:5000"

    def json_response(self, data, status_code=200): 
        """
        Adds json header and status code to response.
            :param data: 
            :param status_code=200: 
        """   
        dataToDict = eval(data) if type(data) is str else data
        dataToDict["code"] = status_code
        self.set_status(status_code)
        self.set_header("Content-Type", 'application/json')
        self.write(dataToDict)

    def json_error(self): 
        self.json_response({'message': 'request body is empty'}, 404)        
    
    def set_default_headers(self):
        """
        http://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler.set_default_headers
        """
        self.set_header("Access-Control-Allow-Origin", self.api_url)
        self.set_header("Access-Control-Allow-Credentials",
                         "true")
        self.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Access-Control-Allow-Headers, Authorization, x-requested-with")
        self.set_header('Access-Control-Allow-Methods',
                        "POST, GET, DELETE, OPTIONS, PUT")
        
    def options(self):
        self.set_status(204)
        self.finish()


def authorised_user(func):
    """
    Get `auth` cookie which should be user_uuid.
    Should contain user information. If it does
    run function and pass user info as arg.
    If not return error.
        :param func: function passed into decorator
    """
    def wrapper(self): 
        cookie_val = self.get_cookie('auth')
        user_info = Users.select_where('user_uuid', cookie_val)
        if user_info:
            func(self, user_info[0])
        else:
            self.json_response({'message': 'not authorised'}, 401)

    return wrapper
