import hashlib

from sqlalchemy.exc import IntegrityError

from opentarock.users import User


class DuplicateEmailError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UserManager:
    def __init__(self, session, hasher, token_generator):
        self.session = session
        self.hasher = hasher
        self.token_generator = token_generator

    def num_users(self):
        return self.session.query(User).count()

    def register_user(self, user):
        self.session.begin_nested()
        self.session.add(user)
        try:
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            if ("unique" in str(e.orig).lower()
               and "email" in str(e.orig).lower()):
                raise DuplicateEmailError("E-mail address already used")
            else:
                raise e

    def authenticate(self, email, plain_password):
        user = self.session.query(User).filter_by(email=email).first()
        if (user
           and user.password == self.hasher.hash(plain_password, user.salt)):
            token = self.token_generator.generate(512)
            return hashlib.sha256(token.encode("ascii")).hexdigest()
        else:
            raise AuthenticationError("Username and password do not match")
