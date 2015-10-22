# -*- coding: utf-8 -*-
from __future__ import print_function

from pprint import pprint

from nltk import NgramTagger
from nltk import jsontags
from nltk.corpus import brown
import nltk


"""
5 章 単語の分類とタグ付け

37. 1つ前のタグ情報を利用するデフォルトタガーを作る

  'I like to blog on Kim's blog' の blog にどうやってタグを付けるか？

  a. 1つ前の単語を調べるが、現在の単語は無視するユニグラムタガーを作る
  b. バックオフタガーに組み込む、組み込むのはデフォルトタガーの直前
  c. 性能がどのぐらいか評価してみる

    ADJ     形容詞          new, good, high, special, big, local
    ADP     接置詞          on, of, at, with, by, into, under
    ADV     副詞            really, already, still, early, now
    CNJ     接続詞          and, or, but, if, while, although
    DET     限定詞          the, a, some, most, every, no, which
    EX      存在詞          there, theres
    FW      外来語          dolce, ersatz, esprit, quo, maitre
    MOD     助動詞          will, can, would, may, must, should
    N       名詞            year, home, costs, time, Africa
    NP      固有名詞        Alison, Africa, April, Washington
    NUM     数詞            twenty-four, fourth, 1991, 14:24
    PRO     代名詞          he, their, her, its, my, I, us
    P       不変化詞        at, on, out, over per, that, up, with
    TO      単語[to_]       to
    UH      間投詞          ah, bang, ha, whee, hmpf, oops
    V       動詞            is, say, told, given, playing, would
    VD      動詞(過去形)    said, took, told, made, asked
    VG      動詞(現在分詞)  making, going, playing, working
    VN      動詞(過去分詞)  given, taken, begun, sung
    WH      wh 限定子       who, which, when, what, where, how
"""


@jsontags.register_tag
class PreviousTagTagger(NgramTagger):

    json_tag = 'nltk.tag.sequential.PreviousTagTagger'

    def __init__(self, train=None, model=None,
                 backoff=None, cutoff=0, verbose=False):
        NgramTagger.__init__(self, 1, train, model,
                             backoff, cutoff, verbose)

    def context(self, tokens, index, history):
        if index == 0:
            previous_tag = None
            return None, tokens[index]
        else:
            previous_tag = history[index - 1]
        return previous_tag, tokens[index]


def evaluate_tagger(tagger, test_sents, unseen_sents):
    def get_backoff_tagger_name(tagger):
        yield repr(tagger)
        backoff_tagger = tagger.backoff
        if backoff_tagger is None:
            raise StopIteration()
        else:
            for name in get_backoff_tagger_name(backoff_tagger):
                yield name

    result = tagger.evaluate(test_sents)
    print(' -> '.join(get_backoff_tagger_name(tagger)))
    pprint(tagger.tag(unseen_sents))
    print('result: %f' % result)
    print('-' * 32)
    print('')


def main():
    brown_tagged_sents = brown.tagged_sents(categories='news')
    brown_sents = brown.sents(categories='news')
    train_size = int(len(brown_tagged_sents) * 0.9)
    train_sents = brown_tagged_sents[:train_size]
    test_sents = brown_tagged_sents[train_size:]
    unseen_sents = brown_sents[train_size + 117]

    # unigram only
    unigram_tagger = nltk.UnigramTagger(train_sents, verbose=True)
    evaluate_tagger(unigram_tagger, test_sents, unseen_sents)

    # previous only
    previous_tagger = PreviousTagTagger(train_sents, verbose=True)
    evaluate_tagger(previous_tagger, test_sents, unseen_sents)

    # default tagger
    t0 = nltk.DefaultTagger('NN')

    # backoff 2
    t1 = nltk.UnigramTagger(train_sents, backoff=t0)
    t2 = nltk.BigramTagger(train_sents, backoff=t1)
    evaluate_tagger(t2, test_sents, unseen_sents)

    # backoff 3
    t1 = nltk.UnigramTagger(train_sents, backoff=t0)
    t2 = nltk.BigramTagger(train_sents, backoff=t1)
    t3 = nltk.TrigramTagger(train_sents, backoff=t2)
    evaluate_tagger(t3, test_sents, unseen_sents)

    # backoff previous 2
    t1 = PreviousTagTagger(train_sents, backoff=t0)
    t2 = nltk.BigramTagger(train_sents, backoff=t1)
    evaluate_tagger(t2, test_sents, unseen_sents)

    # backoff previous 3
    t1 = PreviousTagTagger(train_sents, backoff=t0)
    t2 = nltk.UnigramTagger(train_sents, backoff=t1)
    t3 = nltk.BigramTagger(train_sents, backoff=t2)
    evaluate_tagger(t3, test_sents, unseen_sents)

    # backoff previous 4
    t1 = PreviousTagTagger(train_sents, backoff=t0)
    t2 = nltk.UnigramTagger(train_sents, backoff=t1)
    t3 = nltk.BigramTagger(train_sents, backoff=t2)
    t4 = nltk.TrigramTagger(train_sents, backoff=t3)
    evaluate_tagger(t4, test_sents, unseen_sents)


if __name__ == '__main__':
    main()
