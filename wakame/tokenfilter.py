import logging
from typing import List

from .tokenizer import Token

logger = logging.getLogger(__name__)


class TokenFilter:
    def filter(self, tokens):
        return self.apply(tokens)

    def apply(self, tokens):
        raise NotImplementedError


class POSKeepFilter(TokenFilter):
    """ 指定された品詞を残すフィルター """

    def __init__(self, pos_list):
        """
        Parameters
        ----------
        pos_list : list of str
            品詞のリスト.
        """
        self.pos_list = pos_list

    def apply(self, tokens):
        for token in tokens:
            if any(token.part_of_speech.startswith(pos) for pos in self.pos_list):
                yield token


class POSStopFilter(TokenFilter):
    """ 指定された品詞を落とすフィルター """

    def __init__(self, pos_list):
        """
        Parameters
        ----------
        pos_list : list of str
            品詞のリスト.
        """
        self.pos_list = pos_list

    def apply(self, tokens):
        for token in tokens:
            if any(token.part_of_speech.startswith(pos) for pos in self.pos_list):
                continue
            yield token


class POSReplaceFilter(TokenFilter):
    """ 特定の品詞の単語を指定した文字列に変換する """

    def __init__(self, pos_list, repl):
        self.pos_list = pos_list
        self.replacement = repl

    def apply(self, tokens: List[Token]):
        for token in tokens:
            if any(token.part_of_speech.startswith(pos) for pos in self.pos_list):
                token.surface = self.replacement
                token.base_form = self.replacement
                token.reading = self.replacement
                token.phonetic = self.replacement
            yield token
