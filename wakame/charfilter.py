import re


class CharFilter:
    def filter(self, text):
        return self.apply(text)
    
    def apply(self, text):
        raise NotImplementedError

class RegexReplaceCharFilter(CharFilter):
    def __init__(self, pat, repl):
        self. pattern = re.compile(pat)
        self.replacement = repl
    
    def apply(self, text):
        return re.sub(self.pattern, self.replacement, text)