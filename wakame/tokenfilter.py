import logging
from typing import List

from .tokenizer import Token

logger = logging.getLogger(__name__)


class TokenFilter:
    def filter(self, tokens):
        return self.apply(tokens)

    def apply(self, tokens):
        raise NotImplementedError


class LowerCaseFilter(TokenFilter):
    """
    surfaceとbase_forとを小文字に変換する.
    """

    def apply(self, tokens):
        for token in tokens:
            token.surface = token.surface.lower()
            token.base_form = token.base_form.lower()
            yield token


class UpperCaseFilter(TokenFilter):
    """
    surfaceとbase_formとを大文字に変換する.
    """

    def apply(self, tokens):
        for token in tokens:
            token.surface = token.surface.upper()
            token.base_form = token.base_form.upper()
            yield token


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
            yield token


class RestoreFilter(TokenFilter):
    """ 変換されたsurfaceをもとに戻すフィルター """

    def __init__(self, surface_list):
        self.surface_list = surface_list

    def apply(self, tokens: List[Token]):
        for token in tokens:
            if any(token.cache == surface for surface in self.surface_list):
                token.surface = token.cache
            yield token
