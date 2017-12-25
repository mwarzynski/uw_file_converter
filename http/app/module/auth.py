""" Auth module responsible for user authentication """
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

import bcrypt
import tornado.web
import tornado.gen
import tornado.ioloop
import tornado.escape
from tornado.platform.asyncio import to_tornado_future

LOG = logging.getLogger('auth')
LOG.setLevel(logging.DEBUG)


def blocking(method):
    """Wraps the method in an async method, and executes the function on `self.executor`."""
    @wraps(method)
    async def wrapper(self, *args, **kwargs):
        fut = self.executor.submit(method, self, *args, **kwargs)
        return await to_tornado_future(fut)
    return wrapper


@blocking
def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())


@blocking
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password, hashed_password)


class AuthBaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class LoginHandler(AuthBaseHandler):
    """
    MongoDB collection - users
    user = {
        "username" - login 
        "hashed_password" - bcrypt hashed password
    }
    """
    executor = ThreadPoolExecutor(max_workers=4)

    def initialize(self, mongo):
        self.mongo = mongo

    async def post(self):
        username = self.get_argument("user")
        user_pass = tornado.escape.utf8(self.get_argument("password"))

        user = await self.mongo.users.find_one({
            'username': {'$eq': username}
        })
        if not user:
            LOG.warning("User %s not found", username)
            raise tornado.web.HTTPError(401)

        LOG.debug('Found user %s', username)
        pass_ok = await verify_password(user_pass, tornado.escape.utf8(user["hashed_password"]))

        if not pass_ok:
            LOG.warning("Invalid password for user %s", username)
            raise tornado.web.HTTPError(401)

        LOG.info('Password match for user %s', username)
        self.set_secure_cookie("user", username)


class LogoutHandler(AuthBaseHandler):
    def initialize(self, mongo):
        self.mongo = mongo

    def post(self):
        self.clear_cookie("user")
