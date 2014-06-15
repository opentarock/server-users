@0x82cd5884264305b5;

struct Authenticate {
  email @0 :Text;
  plainPassword @1 :Text;
}

struct AuthenticationSuccess {
  authToken @0 :Text;
}

struct AuthenticationError {
  message @0 :Text;
}
