# wakame
janomeライクなインターフェイスを提供するmecabのラッパーです.

## 利用方法

```python
import MeCab
from wakame.analyzer import Analyzer
from wakame.charfilter import *
from wakame.tokenfilter import *

text = '和布ちゃんこんにちは'
# 基本的な使い方
analyzer = Analyzer()
tokens = analyzer.analyze(text)

# 辞書をNEologdにする場合
analyzer = Analyzer(use_neologd=True)
tokens = analyzer.analyze(text)

# filterを利用する場合
char_filters = [RegexReplaceCharFilter('和布', 'wakame')]
token_filters = [POSKeepFilter('名詞'), POSStopFilter(['名詞,接尾'])]
analyzer = Analyzer(char_filters=char_filters, token_filters=token_filters)
tokens = analyzer.analyze(text)

```

## インストール

### MeCabのインストール(必須)
```sh
brew install mecab
brew install mecab-ipadic
```

### mecab-ipadic-NEologdのインストール(任意)
```sh
brew install git curl xz
git clone --depth 1 git@github.com:neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd
./bin/install-mecab-ipadic-neologd -n
```
詳しくは[こちらを参照してください](https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md)

### mecab-python3のインストール(必須)
```sh
brew install swig
pip install mecab-python3
```

## wakameのインストール(必須)

```sh
pip install wakame
```