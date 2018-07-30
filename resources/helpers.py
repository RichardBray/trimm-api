from tornado.web import RequestHandler
from models.mysql import Users

class PageHandler(RequestHandler):
    def json_response(self, data, status_code=200): 
        """
        Adds json header and status code to response.
            :param data: 
            :param status_code=200: 
        """   
        self.set_status(status_code)
        self.set_header("Content-Type", 'application/json')
        self.write(data)

    def json_error(self): 
        self.json_response({'message': 'request body is empty'}, 404)        
    
    def set_default_headers(self):
        """
        http://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler.set_default_headers
        """
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

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
