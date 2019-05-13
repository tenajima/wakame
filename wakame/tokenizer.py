import re
import subprocess

import MeCab


class Token:
    """
    tokenの情報を内包するクラス
    """

    def __init__(self, word_with_feat: str):
        surface, feature = word_with_feat.split("\t")

        # mecabの仕様で,アルファベットの単語は原型が'*'になり,
        # 読みと発音が省略されるためその対応として以下のように行う.
        split_feature = feature.split(",")
        if len(split_feature) == 7:
            part_of_speech = ",".join(split_feature[:4])
            infl_type = split_feature[4]
            infl_form = split_feature[5]
            base_form = surface
            reading = "*"
            phonetic = "*"
        else:
            (
                part_of_speech,
                infl_type,
                infl_form,
                base_form,
                reading,
                phonetic,
            ) = feature.rsplit(",", 5)

        self.surface = surface
        """surface form (表層形)"""
        self.part_of_speech = part_of_speech
        """part of speech (品詞)"""
        self.infl_type = infl_type
        """terminal form (活用型)"""
        self.infl_form = infl_form
        """stem form (活用形)"""
        self.base_form = base_form
        """base form (基本形)"""
        self.reading = reading
        """"reading (読み)"""
        self.phonetic = phonetic
        """pronounce (発音)"""

    def __str__(self):
        return "%s\t%s,%s,%s,%s,%s,%s" % (
            self.surface,
            self.part_of_speech,
            self.infl_type,
            self.infl_form,
            self.base_form,
            self.reading,
            self.phonetic,
        )


class Tokenizer:
    """
    textの品詞分解を司るクラス
    """

    def __init__(self, use_neologd=False):
        """mecabを使えるようにする

        Parameters
        ----------
        use_neologd : bool, optional
            NEologdを使うかどうかを指定する, by default False
        """
        # get neologd
        cmd = "echo `mecab-config --dicdir`"
        if use_neologd:
            cmd = cmd + '"/mecab-ipadic-neologd"'
        else:
            cmd = cmd + '"/ipadic"'

        # 辞書のパスを取得する
        dict_path = (
            subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            .stdout.readline()
            .decode()
        )
        dict_path = re.sub(r"\n", "", dict_path)

        self.tokenizer = MeCab.Tagger("-d " + dict_path)

    def tokenize(self, text, wakati=False):
        """トークン化する

        Parameters
        ----------
        text : str
            品詞分解する対象のtext
        wakati : bool, optional
            Trueにするとsurface部分のみをリストで返すようにする, by default False

        Returns
        -------
        トークンのリスト(wakati=False),もしくは文字列のリスト(wakati=True)
        """
        chunk: str = self.tokenizer.parse(text).split("\n")[:-2]
        if wakati:
            tokens = [Token(ch).surface for ch in chunk]
        else:
            tokens = [Token(ch) for ch in chunk]
        return tokens
