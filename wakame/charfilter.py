import re


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


class URLReplaceFilter(RegexReplaceCharFilter):
    def __init__(self, repl=""):
        self.pattern = re.compile(
            r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)"
        )
        self.replacement = repl
