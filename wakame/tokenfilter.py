import pandas as pd


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

    def apply(self, tokens: pd.DataFrame):
        return tokens[tokens['part_of_speech'].str.match(
            f"({'|'.join(self.pos_list)})")]


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

    def apply(self, tokens: pd.DataFrame):
        return tokens[~tokens['part_of_speech'].str.
                      match(f"({'|'.join(self.pos_list)})")]
