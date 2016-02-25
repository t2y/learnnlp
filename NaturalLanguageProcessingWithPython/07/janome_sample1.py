# -*- coding: utf-8 -*-
from __future__ import print_function

from janome.tokenizer import Tokenizer


def main():
    """
    >>> main()
    すもも	名詞,一般,*,*,*,*,すもも,スモモ,スモモ
    も	助詞,係助詞,*,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,*,もも,モモ,モモ
    も	助詞,係助詞,*,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,*,もも,モモ,モモ
    の	助詞,連体化,*,*,*,*,の,ノ,ノ
    うち	名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ
    """
    t = Tokenizer()
    for token in t.tokenize(u'すもももももももものうち'):
        print(token)


if __name__ == '__main__':
    main()
