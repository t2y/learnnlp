# -*- coding: utf-8 -*-

# ---

>>> l = range(10)
>>> l[:3] = []
>>> l
[3, 4, 5, 6, 7, 8, 9]


# ---
"""
3.4 から標準ライブラリに statistics が入ってる
"""
from backports.statistics import mean

mean([1, 3, 5])
mean(range(1, 10))

# ---
"""
単語の平均文字数を調べる
"""
from nltk.corpus import brown
words = brown.words(categories='adventure')
mean(map(len, words))

# ---
"""
カテゴリを調べる
"""
brown.categories()
