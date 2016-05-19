# -*- coding: utf-8 -*-

"""
素性ベース文法の定義と確認

* 文法ファイルに定義を記述してトークンを与えて構文解析してみる
"""

from nltk import load_parser

token1 = 'I am happy'.split()

cp8 = load_parser('grammer8.fcfg')
cp20 = load_parser('grammer20.fcfg', trace=1)

for i in cp8.parse(token1):
    print(i)

for i in cp20.parse(token1):
    print(i)
