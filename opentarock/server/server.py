import logging

import capnp

from opentarock.users import User
from opentarock.users.user_manager import (
    DuplicateEmailError,
    AuthenticationError)

capnp.remove_import_hook()
register_capnp = capnp.load('messages/register.capnp')
auth_capnp = capnp.load('messages/authenticate.capnp')

logger = logging.getLogger(__name__)


REGISTER_MESSAGE_TYPE = 1

AUTHENTICATE_MESSAGE_TYPE = 2

DUPLICATE_EMAIL_ERROR = register_capnp.RegisterError.new_message(
    message="Email address already used",
    error='duplicateEmail')

AUTHENTICATION_ERROR = auth_capnp.AuthenticationError.new_message(
    message="Email and password do not match")


def create_success_msg(user_id):
    return register_capnp.RegisterSuccess.new_message(
        userId=user_id)


class Server:
    __run = False

    def __init__(self, rep_socket, hasher, token_generator, user_manager):
        self.rep_socket = rep_socket
        self.hasher = hasher
        self.token_generator = token_generator
        self.user_manager = user_manager

    def start(self):
        self.__run = True
        rep_socket_bind = 'tcp://*:6000'
        logger.info("Binding server socket to {}".format(rep_socket_bind))
        self.rep_socket.bind(rep_socket_bind)

        self._receive_loop(self._message_handler)

        self.rep_socket.close()

    def _receive_loop(self, msg_handler):
        while self.is_running():
            msg = self.rep_socket.recv()
            logger.debug("Received message of length {:d}".format(len(msg)))
            if len(msg) < 1:
                reply = b'\xff'
            else:
                try:
                    reply = msg_handler(self, msg[0], msg[1:]).to_bytes()
                except ValueError:
                    reply = b'\xff'
            self.rep_socket.send(reply)

    @staticmethod
    def _message_handler(self, msg_type, msg):
        logger.debug("Handling message of type {:02x}")
        if msg_type == REGISTER_MESSAGE_TYPE:
            return handle_message_register(self, msg)
        elif msg_type == AUTHENTICATE_MESSAGE_TYPE:
            return handle_message_authenticate(self, msg)
        else:
            raise ValueError("Unknown message type: {:02x}".format(msg_type))

    def is_running(self):
        return self.__run


def handle_message_register(self, msg):
    register_message = register_capnp.Register.from_bytes(msg)
    user = User.from_message(register_message,
                             self.hasher,
                             self.token_generator)
    try:
        user_id = self.user_manager.register_user(user)
        logger.info("Registration successfull: {}".format(user.email))
        return create_success_msg(user_id)
    except DuplicateEmailError:
        logger.info("Can't register user with email {}: " +
                    "duplicate email".format(user.email))
        return DUPLICATE_EMAIL_ERROR


def auth_success_msg(token):
    return auth_capnp.AuthenticationSuccess.new_message(authToken=token)


def handle_message_authenticate(self, msg):
    auth_msg = auth_capnp.Authenticate.from_bytes(msg)
    try:
        token = self.user_manager.authenticate(auth_msg.email,
                                               auth_msg.plainPassword)
        logger.info("Authentication successfull: {}".format(auth_msg.email))
        return auth_success_msg(token)
    except AuthenticationError:
        logger.info("Authentication failure: {}".format(auth_msg.email))
        return AUTHENTICATION_ERROR
