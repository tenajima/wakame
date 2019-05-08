import logging
import re
import subprocess

import MeCab
import pandas as pd

from .tokenizer import Tokenizer, Token

logger = logging.getLogger(__name__)


class Analyzer:
    def __init__(self, tokenizer: Tokenizer, char_filters=[],
                 token_filters=[]):
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

    def analyze(self, text: str):
        """品詞に分解するメソッド.
        
        Parameters
        ----------
        text : str
            解析する文字列
        
        Returns
        -------
        pd.DataFrame
            解析結果
            surface, part_of_speech, base_formのカラムを持ったDataFrameに分解する.
        """
        for cfilter in self.char_filters:
            text = cfilter.filter(text)

        tokens = self.tokenizer.tokenize(text)
        for tfilter in self.token_filters:
            tokens = tfilter.filter(tokens)

        return tokens
