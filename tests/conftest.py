import capnp
from unittest.mock import Mock

import pytest

from opentarock.users import User, Hasher, UserManager
from opentarock.users.token_generator import TokenGenerator

from opentarock.server import Server

capnp.remove_import_hook()
register_capnp = capnp.load('messages/register.capnp')
auth_capnp = capnp.load('messages/authenticate.capnp')


@pytest.fixture
def hasher():
    return Hasher()


@pytest.fixture
def hasher_mock():
    return Mock()


@pytest.fixture
def token_generator():
    return TokenGenerator()


@pytest.fixture
def token_generator_mock():
    return Mock()


@pytest.fixture
def rep_socket():
    return Mock()


@pytest.fixture
def session():
    return Mock()


@pytest.fixture
def user_manager(session, hasher_mock, token_generator):
    return UserManager(session, hasher_mock, token_generator_mock)


@pytest.fixture
def server(rep_socket, hasher, token_generator, user_manager):
    return Server(rep_socket, hasher, token_generator, user_manager)


@pytest.fixture(scope='function')
def random_user(hasher):
    plain_password = "password"
    salt = "salt"
    password = hasher.hash(plain_password, salt)
    return User(email="email@example.com", display_name="username",
                salt=salt, password=password)


@pytest.fixture(scope='function')
def user(hasher):
    plain_password = "password"
    salt = "salt"
    password = hasher.hash(plain_password, salt)
    return User(email="email@example.com", display_name="name",
                salt=salt, password=password)


@pytest.fixture(scope='function')
def register_msg(hasher):
    msg = register_capnp.Register.new_message(email="email@example.com",
                                              plainPassword="password",
                                              displayName="name")
    return msg


@pytest.fixture(scope='function')
def authenticate_msg():
    msg = auth_capnp.Authenticate.new_message(email="auth@example.com",
                                              plainPassword="auth")
    return msg
