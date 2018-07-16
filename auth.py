import jwt

secret_key = "secret"


def return_auth_error(handler, message):
    """
        Return authorization error 
    """
    handler._transforms = []
    handler.set_status(401)
    handler.write(message)
    handler.finish()


def jwtauth(handler_class):
    """
        Tornado JWT Auth Decorator
        https://github.com/vsouza/JWT-Tornado/blob/master/auth.py
        https://github.com/paulorodriguesxv/tornado-json-web-token-jwt/blob/master/auth.py
    """
    def require_auth(handler):
        auth = handler.request.headers.get('Authorization')
        if auth:
            parts = auth.split()
            token = parts[1]

            try:
                jwt.decode(token, secret_key, algorithms='HS256')
            except Exception as err:
                print(err)

        else:
            handler._transforms = []
            handler.write("Missing authorization")
            handler.finish()

        return True

