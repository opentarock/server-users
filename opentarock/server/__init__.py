import logging.config

import yaml
from nanomsg import Socket, REP
import sqlalchemy

from opentarock.users import Hasher, UserManager
from opentarock.users.token_generator import TokenGenerator
from opentarock.server.server import Server

engine = sqlalchemy.create_engine('sqlite:////sqlite/users.db')
Session = sqlalchemy.orm.sessionmaker(bind=engine)


def setup_logging(log_config):
    with open(log_config, 'rt') as f:
        config = yaml.load(f.read())
        logging.config.dictConfig(config)


def main():
    setup_logging("config/logging.yml")

    rep_socket = Socket(REP)
    hasher = Hasher()
    token_generator = TokenGenerator()
    session = Session()
    user_manger = UserManager(session, hasher, token_generator)
    server = Server(rep_socket, hasher, token_generator, user_manger)
    server.start()


if __name__ == "__main__":
    main()
