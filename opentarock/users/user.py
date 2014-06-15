from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

SALT_LENGTH = 128


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    email = Column(String(250), unique=True)

    display_name = Column(String(50))

    salt = Column(String(128))

    password = Column(String(32))

    def __repr__(self):
        return ("<User(id={0}, email='{1}', display_name='{2}', " +
                "salt='{3}', password='{4}')>").format(
                    self.id,
                    self.email,
                    self.display_name,
                    self.salt,
                    self.password)

    def __eq__(self, other):
        return (self.id == other.id and
                self.email == other.email and
                self.display_name == other.display_name and
                self.salt == other.salt,
                self.password == other.password)

    @staticmethod
    def from_message(msg, hasher, token_generator):
        salt = token_generator.generate(SALT_LENGTH)
        user = User(email=msg.email,
                    display_name=msg.displayName,
                    salt=salt,
                    password=hasher.hash(msg.plainPassword, salt))
        return user
