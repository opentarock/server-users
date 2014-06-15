@0xdc6e48e9b05c74cc;

struct Register {
  email @0 :Text;
  plainPassword @1 :Text;
  displayName @2 :Text;
}

struct RegisterSuccess {
  userId @0 :UInt32;
}

struct RegisterError {
  message @0 :Text;
  error @1 :Error;

  enum Error {
    duplicateEmail @0;
  }
}
