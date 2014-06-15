import pytest


class TestHasher:
    @pytest.mark.randomize(data=str, salt1=str, salt2=str, ncalls=1)
    def test_hashing_data_with_different_salts(self, hasher, data,
                                               salt1, salt2):
        if salt1 == salt2:
            salt1 += "x"
        assert hasher.hash(data, salt1) != \
            hasher.hash(data, salt2)

    def test_hash_value_for_str_and_bytes_is_the_same(self, hasher):
        assert hasher.hash("abc", "salt") == hasher.hash(b"abc", b"salt")
