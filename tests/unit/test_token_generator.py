import random

from unittest.mock import MagicMock

from opentarock.users.token_generator import TokenGenerator


class TestTokenGenerator:
    def test_generate_has_a_default_length(self, token_generator):
        assert len(token_generator.generate()) == 32

    def test_generates_token_of_correct_length(self, token_generator):
        assert len(token_generator.generate(5)) == 5

    def test_generate_token_with_custom_characters(self):
        token_generator = TokenGenerator(chars='a')
        assert token_generator.generate(10) == 'a'*10

    def test_generator_uses_chosen_random_generator(self):
        random_gen = random.SystemRandom()
        random_gen.choice = MagicMock(return_value='b')
        token_generator = TokenGenerator(rand_gen=random_gen,
                                         chars='abc')
        token_generator.generate(8)
        random_gen.choice.assert_called_with('abc')
        assert random_gen.choice.call_count == 8
