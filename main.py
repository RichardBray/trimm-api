from tornado.web import Application, HTTPError, RequestHandler
from tornado.ioloop import IOLoop
from resources.user import UserRegister, UserLogin, UserEdit, UserLogout, AuthenticateUser
from resources.categories import AllCategories, Category
from resources.spending import SpendingItems, SpendingItem
from tornado.options import parse_config_file
import logging as log

port_number = 3000

class BadRequestHandler(RequestHandler):
    def get(self):
        raise HTTPError(400)


class InitialiseApp(Application):
    def __init__(self):
        handlers = [
            (r"/register", UserRegister),
            (r"/login", UserLogin),
            (r"/logout", UserLogout),
            (r"/auth", AuthenticateUser),
            (r"/user-edit", UserEdit),
            (r"/items", SpendingItems),
            (r"/item", SpendingItem),
            (r"/categories", AllCategories),
            (r"/category", Category),
            (r"/.*", BadRequestHandler),
        ]

        server_settings = {
            "debug": True,
            "autoreload": True
        }

        Application.__init__(self, handlers, **server_settings)


def run_server():
    app = InitialiseApp()
    app.listen(port_number)
    IOLoop.instance().start()
    


if __name__ == '__main__':
    parse_config_file("./config/local.conf")
    start_message = "Server running on port:{}".format(port_number)
    log.info(start_message)
    run_server()
