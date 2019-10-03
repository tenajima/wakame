import logging
from typing import List

import pandas as pd

from .tokenizer import Tokenizer, Token

logger = logging.getLogger(__name__)


class Analyzer:
    def __init__(self, tokenizer: Tokenizer, char_filters=[], token_filters=[]):
        """Analyzer Object

        Parameters
        ----------
        tokenizer: Tokenizer
            Tokenizer object
        char_filters : list, optional
            CharFilters list, by default []
        token_filters : list, optional
            TokenFilters list, by default []
        """

        self.tokenizer = tokenizer
        self.char_filters = char_filters
        self.token_filters = token_filters

    def analyze(self, text: str, wakati: bool = False):
        """品詞に分解するメソッド.

        Parameters
        ----------
        text : str
            解析する文字列
        wakati: bool, optional
            Trueにするとsurface部分のみをリストで返すようにする

        Returns
        -------
        トークンのジェネレーター
        """

        if not text:
            logger.info("text is empty!")
            return
        for cfilter in self.char_filters:
            text = cfilter.filter(text)

        tokens: List[Token] = self.tokenizer.tokenize(text)
        for tfilter in self.token_filters:
            tokens = tfilter.filter(tokens)

        if wakati:
            return [token.surface for token in tokens]

        return tokens

    def analyze_with_dataframe(self, text: str):
        """品詞分解したものをpd.DataFrameで返すメソッド

        Parameters
        ----------
        text : str
            解析する文字列

        Returns
        -------
        pd.DataFrame
        """
        if not text:
            logger.info("text is empty!")
            return

        tokens: List[Token] = list(self.analyze(text))
        try:
            columns = list(tokens[0].__dict__.keys())
        except IndexError:
            columns = [
                "surface",
                "part_of_speech",
                "infl_type",
                "infl_form",
                "base_form",
                "reading",
                "phonetic",
            ]
            return pd.DataFrame(columns=columns)

        dataframe = {}
        for col in columns:
            if col != "cache":
                dataframe[col] = [getattr(token, col) for token in tokens]

        return pd.DataFrame(dataframe)
