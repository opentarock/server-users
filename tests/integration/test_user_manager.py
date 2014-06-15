import copy

import pytest

from sqlalchemy.exc import IntegrityError

from opentarock.users.user_manager import (
    DuplicateEmailError,
    AuthenticationError)


class TestUserManager():
    def test_user_is_inserted_into_database(self, random_user, user_manager):
        user_manager.register_user(random_user)
        assert random_user.id > 0
        assert user_manager.num_users() == 1

    def test_two_users_with_the_same_email_are_not_allowed(self,
                                                           random_user,
                                                           user_manager):
        random_user2 = copy.deepcopy(random_user)
        user_manager.register_user(random_user)
        with pytest.raises(DuplicateEmailError):
            user_manager.register_user(random_user2)
        assert user_manager.num_users() == 1

    def test_registred_user_can_authenticate(self, random_user, user_manager):
        user_manager.register_user(random_user)
        session_id = user_manager.authenticate(random_user.email, "password")
        assert len(session_id) == 64

    def test_unregistered_user_cant_authenticate(self, random_user,
                                                 user_manager):
        with pytest.raises(AuthenticationError):
            session_id = \
                user_manager.authenticate(random_user.email, "password")
            assert session_id is None

    def test_registered_user_with_wrong_password_cant_authenticate(
            self, random_user, user_manager):
        user_manager.register_user(random_user)
        with pytest.raises(AuthenticationError):
            session_id = user_manager.authenticate(random_user.email, "wrong")
            assert session_id is None

    def test_registering_a_user_with_a_missing_field_fails(
            self, random_user, user_manager):
        random_user.password = None
        with pytest.raises(IntegrityError):
            user_manager.register_user(random_user)
