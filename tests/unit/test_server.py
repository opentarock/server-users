from unittest.mock import Mock, MagicMock

from opentarock.users.user_manager import (
    DuplicateEmailError,
    AuthenticationError)
from opentarock.server import Server


class TestServer:
    def test_new_server_is_not_started(self, server):
        assert server.is_running() is False

    def test_server_is_bound_to_correct_address(self, server):
        def noop_receive_loop(msg_handler):
            pass
        server._receive_loop = noop_receive_loop
        server.rep_socket.bind = MagicMock()
        server.rep_socket.close = MagicMock()

        server.start()

        server.rep_socket.bind.assert_called_once_with("tcp://*:6000")
        server.rep_socket.close.assert_called_once_with()

    def test_receive_loop_passes_received_message_to_message_handler(
            self, server):
        # Mock the method is_running so only one iteration of the receive
        # loop is executed
        server.is_running = MagicMock(side_effect=[True, False])

        server.rep_socket.recv = MagicMock(return_value=b"\x01data")
        server.rep_socket.send = MagicMock()
        reply = Mock()
        reply.to_bytes = MagicMock(return_value=b"reply")
        message_handler = MagicMock(return_value=reply)

        server._receive_loop(message_handler)

        server.rep_socket.recv.assert_called_once_with()
        message_handler.assert_called_once_with(server, 1, b"data")
        server.rep_socket.send.assert_called_once_with(b"reply")
        reply.to_bytes.assert_called_once_with()

    def test_receiving_empty_message_replies_with_message_error(self, server):
        server.is_running = MagicMock(side_effect=[True, False])
        server.rep_socket.recv = MagicMock(return_value=b"")
        server.rep_socket.send = MagicMock()
        reply = Mock()
        reply.to_bytes = MagicMock(return_value=b"reply")
        message_handler = MagicMock(return_value=reply)

        server._receive_loop(message_handler)

        server.rep_socket.recv.assert_called_once_with()
        server.rep_socket.send.assert_called_once_with(b"\xff")

    def test_receiving_corrupted_message_results_in_error_message(
            self, register_msg, server):
        server.is_running = MagicMock(side_effect=[True, False])
        server.rep_socket.recv = MagicMock(
            return_value=b'\x01' + register_msg.to_bytes()[1:])
        server.rep_socket.send = MagicMock()

        server._receive_loop(Server._message_handler)

        server.rep_socket.recv.assert_called_once_with()
        server.rep_socket.send.assert_called_once_with(b"\xff")

    def test_message_handler_returns_error_response_if_message_if_unknown_type(
            self, server):
        server.is_running = MagicMock(side_effect=[True, False])
        server.rep_socket.recv = MagicMock(
            return_value=b'\x00')
        server.rep_socket.send = MagicMock()

        server._receive_loop(Server._message_handler)

        server.rep_socket.recv.assert_called_once_with()
        server.rep_socket.send.assert_called_once_with(b"\xff")

    def test_user_is_registered_after_receiving_register_message(
            self, user, register_msg, server):
        server.user_manager.register_user = MagicMock(return_value=10)
        server.token_generator.generate = MagicMock(return_value="salt")

        response = Server._message_handler(server, 1, register_msg.to_bytes())

        server.user_manager.register_user.assert_called_once_with(user)
        assert response.userId == 10

    def test_registration_error_is_returned_if_email_is_alredy_used(
            self, user, register_msg, server):
        server.user_manager.register_user = MagicMock(
            side_effect=DuplicateEmailError())
        result = Server._message_handler(server, 1, register_msg.to_bytes())
        assert result.error == 'duplicateEmail'

    def test_successful_user_authentication_returns_success_message(
            self, authenticate_msg, server):
        server.user_manager.authenticate = MagicMock(return_value="token")
        result = Server._message_handler(server,
                                         2, authenticate_msg.to_bytes())
        assert result.authToken == "token"

    def test_authentication_returns_error_if_wrong_credentials(
            self, authenticate_msg, server):
        server.user_manager.authenticate = MagicMock(
            side_effect=AuthenticationError())
        result = Server._message_handler(server,
                                         2, authenticate_msg.to_bytes())
        assert len(result.message) > 5
