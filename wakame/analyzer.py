import logging
import re
import subprocess

import MeCab
import pandas as pd

logger = logging.getLogger(__name__)


class Analyzer:
    def __init__(self, char_filters=[], token_filters=[], use_neologd=False):
        """Analyzer Object
        
        Parameters
        ----------
        char_filters : list, optional
            CharFilters list, by default []
        token_filters : list, optional
            TokenFilters list, by default []
        use_neologd : boolean, by default False
            use Neologd dictionary or not
        """

        # get neologd
        cmd = 'echo `mecab-config --dicdir`'
        if use_neologd:
            cmd = cmd + '"/mecab-ipadic-neologd"'
        else:
            cmd = cmd + '"/ipadic"'

        # 辞書のパスを取得する
        dict_path = subprocess.Popen(
            cmd, stdout=subprocess.PIPE,
            shell=True).stdout.readline().decode()
        dict_path = re.sub(r'\n', '', dict_path)

        self.tokenizer = MeCab.Tagger('-d ' + dict_path)
        self.char_filters = char_filters
        self.token_filters = token_filters

    def analyze(self, text: str):
        for cfilter in self.char_filters:
            text = cfilter.filter(text)

        tokens = self.parse(text)

        for tfilter in self.token_filters:
            tokens = tfilter.filter(tokens)

        return tokens

    def parse(self, text: str):
        def make_tmp_columns(text: str):
            """中間カラムをつくるための関数
            
            Parameters
            ----------
            text: str
                mecabでパースしたfeature部分
            Returns
            -------
            str
                ダンダーで区切った中間カラムの文字列
            """
            splits = text.split(',')
            return ','.join(splits[:-3]) + ',__' + splits[-3]

        # mecabを用いてパースする
        chunk: str = self.tokenizer.parse(text)

        # TODO: streamできないと大量の文字が来たときに死んでしまう
        tokens = []
        # うまく分離できなかったものをカウントする
        pass_count = 0
        # 最後の行はEOSのため最後の1つ前のとこまで追加する.
        for word in chunk.splitlines()[:-1]:
            try:
                (surface, feature) = word.split('\t')
            except ValueError:
                pass_count += 1

            tokens.append([surface, feature])
        if pass_count:
            logger.info(f'pass count is: {pass_count}')

        # pd.DataFrameとする
        tokens = pd.DataFrame(tokens, columns=['surface', 'feature'])

        # 中間カラムの生成
        tokens['tmp'] = tokens['feature'].map(
            lambda feat: make_tmp_columns(feat))

        del tokens['feature']

        # 品詞とbase_formの作成
        tokens['part_of_speech'] = tokens['tmp'].map(
            lambda feat: re.sub(r'[\*]+,', '', feat.split('__')[0]))
        tokens['base_form'] = tokens['tmp'].map(
            lambda feat: feat.split('__')[1])

        del tokens['tmp']

        # base_formが"*"のものはsurfaceを採用する
        non_base_form_idx = tokens['base_form'] == '*'
        tokens.loc[non_base_form_idx, 'base_form'] = tokens.loc[
            non_base_form_idx, 'surface']

        return tokens

