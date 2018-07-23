from tornado.web import RequestHandler
from models.mysql import Users

class PageHandler(RequestHandler):
    def json_response(self, data, status_code=200): 
        self.set_status(status_code)
        self.set_header("Content-Type", 'application/json')
        self.write(data)

    def json_error(self):
        self.json_response({'message': 'request body is empty'}, 404)        


def authorised_user(func):
    '''
        Get `auth` cookie which should be user_uuid.
        Should contain user information. If it does
        run function and pass user info as arg.
        If not return error.
    '''
    def wrapper(self):
        cookie_val = self.get_cookie('auth')
        user_info = Users.select_where('user_uuid', cookie_val)
        if user_info:
            func(self, user_info[0])
        else:
            self.json_response({'message': 'not authorised'}, 401)

    return wrapper
