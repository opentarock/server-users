import string

from Crypto.Random.random import StrongRandom


class TokenGenerator:
    def __init__(self, rand_gen=StrongRandom(), chars=string.printable):
        self.rand_gen = rand_gen
        self.chars = chars

    def generate(self, length=32):
        return ''.join(self.rand_gen.choice(self.chars)
                       for _ in range(length))
