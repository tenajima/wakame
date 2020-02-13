import pytest

from wakame.tokenizer import Tokenizer


class TestTokenizer:
    @pytest.fixture
    def tokenizer(self):
        return Tokenizer(use_neologd=False)

    def test_tokenize(self, tokenizer: Tokenizer):
        text = "こんにちは世界"
        expect = ["こんにちは", "世界"]
        result = tokenizer.tokenize(text, wakati=True)
        assert expect == result
