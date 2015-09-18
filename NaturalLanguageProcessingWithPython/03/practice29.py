# -*- coding: utf-8 -*-
from backports.statistics import mean
from nltk.corpus import brown


def calculate_len_mean(iterable):
    """
    >>> calculate_len_mean(['abc', 'd', 'ef'])
    2.0
    >>> calculate_len_mean(['abcde', 'fgh', 'ij'])
    3.3333333333333335
    >>> calculate_len_mean([[1, 2, 3], [4], [5, 6]])
    2.0
    """
    return mean(map(len, iterable))


def calculate_ari(words, sents):
    words_mean = calculate_len_mean(words)
    sents_mean = calculate_len_mean(sents)
    return (4.71 * words_mean) + (0.5 * sents_mean) - 21.43


def calculate_brown_ari(category):
    words = brown.words(categories=category)
    sents = brown.sents(categories=category)
    return calculate_ari(words, sents)


def main():
    for category in brown.categories():
        print('%s: %f' % (category, calculate_brown_ari(category)))


if __name__ == '__main__':
    main()
