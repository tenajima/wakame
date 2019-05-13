import re
import unicodedata


class CharFilter:
    def filter(self, text):
        return self.apply(text)

    def apply(self, text):
        raise NotImplementedError


class RegexReplaceCharFilter(CharFilter):
    def __init__(self, pat, repl):
        """正規表現に一致する部分を置き換える.

        Parameters
        ----------
        pat : str
            文字列型の正規表現.
        repl : str
            置き換える文字列.
        """
        self.pattern = re.compile(pat)
        self.replacement = repl

    def apply(self, text):
        return re.sub(self.pattern, self.replacement, text)


class UnicodeNormalizeCharFilter(CharFilter):
    """
    ユニコード文字列の正規化を行うフィルター
    """

    def __init__(self, form="NFKC"):
        """

        Parameters
        ----------
        form : str, optional
            正規化の形式. 'NFC', 'NFKC, 'NFD'のどれかを選ぶこと. by default 'NFKC'
        """
        self.form = form

    def apply(self, text):
        return unicodedata.normalize(self.form, text)


class URLReplaceFilter(RegexReplaceCharFilter):
    """ URLを指定された文字列に変換するフィルター """
    def __init__(self, repl=""):
        self.pattern = re.compile(
            r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)"
        )
        self.replacement = repl
