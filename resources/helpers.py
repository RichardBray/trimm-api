from tornado.web import RequestHandler


class PageHandler(RequestHandler):
    def json_response(self, data, status_code=200):  # how many before *args?
        self.set_status(status_code)
        self.set_header("Content-Type", 'application/json')
        self.write(data)

    def json_error(self):
        self.json_response({'message': 'request body is empty'}, 404)        
