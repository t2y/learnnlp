# -*- coding: utf-8 -*-
from __future__ import print_function

from nltk import load_parser


"""
9 章 素性ベースの文法の構築

1. "I am happy" や "She is happy" が正しく構文解析でき、"*you is happy" や
   "*they am happy" が正しくないと判断できるためにどのような制約が必要だろうか？
   文法(8)と文法(20)を利用してやってみよう

    文法(8)

        S -> NP_SG VP_SG
        S -> NP_PL VP_PL
        NP_SG -> Det_SG N_SG
        NP_PL -> Det_PL N_PL
        VP_SG -> V_SG
        VP_PL -> V_PL

        Det_ST -> 'this'
        Det_PL -> 'these'
        N_SG -> 'dog'
        N_PL -> 'dogs'
        V_SG -> 'runs'
        V_PL -> 'run'

    文法(20)

        S -> NP[AGR=?n] VP[AGR=?n]
        NP[AGR=?n] -> PropN[AGR=?n]
        VP[TENSE=?t, AGR=?n] -> Cop[TENSE=?t, AGR=?n] Adj

        Cop[TENSE=pres, AGR=[NUM=sg, PER=3]] -> 'is'
        PropN[AGR=[NUM=sg, PER3]] -> 'Kim'
        Adj -> 'happy'

    Feature Grammar Parsing
    http://www.nltk.org/howto/featgram.html

"""


def parse_and_print(chart_parser, tokens):
    print(' '.join(tokens))
    for i in chart_parser.parse(tokens):
        print(i)
    print()


def main():
    test_data = [
        'I am happy'.split(),
        'she is happy'.split(),
        'you are happy'.split(),
        'you is happy'.split(),
    ]

    print('grammer (8)')
    cp8 = load_parser('grammer8.fcfg')
    for tokens in test_data:
        parse_and_print(cp8, tokens)

    print('grammer (20)')
    cp20 = load_parser('grammer20.fcfg', trace=1)
    for tokens in test_data:
        parse_and_print(cp20, tokens)


if __name__ == '__main__':
    main()
