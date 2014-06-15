from unittest.mock import MagicMock

import capnp

from opentarock.users import User

capnp.remove_import_hook()
register_capnp = capnp.load('messages/register.capnp')


class TestUser:
    def test_create_user_from_register_message(self, hasher, token_generator):
        token_generator.generate = MagicMock(return_value="salt")
        hasher.hash = MagicMock(return_value="hash")

        register_message = register_capnp.Register.new_message()
        register_message.email = "mail@example.com"
        register_message.displayName = "Name"
        register_message.plainPassword = "password"
        user = User.from_message(register_message, hasher, token_generator)

        token_generator.generate.assert_called_once_with(128)
        hasher.hash.assert_called_once_with("password", "salt")

        assert user.email == register_message.email
        assert user.display_name == register_message.displayName
        assert user.password == "hash"

    def test_user_has_a_custom_repr(self):
        user = User()
        assert user.__repr__().startswith("<User")
