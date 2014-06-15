import os

import pytest
import sqlalchemy
from alembic.command import upgrade
from alembic.config import Config

from opentarock.users.user_manager import UserManager


def apply_migrations():
    config = Config('alembic.ini')
    upgrade(config, 'head')


@pytest.fixture(scope='session')
def engine(request):
    DB_LOCATION = '/sqlite/users.db'
    engine = sqlalchemy.create_engine('sqlite:///' + DB_LOCATION,
                                      connect_args={'isolation_level': None})
    apply_migrations()

    def finalizer():
        if os.path.exists(DB_LOCATION):
            os.unlink(DB_LOCATION)
    request.addfinalizer(finalizer)
    return engine


@pytest.fixture(scope='function')
def session(request, engine):
    connection = engine.connect()
    transaction = connection.begin()

    Session = sqlalchemy.orm.sessionmaker()
    session = Session(bind=connection)
    session.begin_nested()

    @sqlalchemy.event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    def finalizer():
        session.close()
        transaction.rollback()
        connection.close()
    request.addfinalizer(finalizer)

    return session


@pytest.fixture(scope='function')
def user_manager(session, hasher, token_generator):
    return UserManager(session, hasher, token_generator)
