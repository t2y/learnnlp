# -*- coding: utf-8 -*-
from nltk import FreqDist
from nltk.corpus import gutenberg
from nltk.corpus import inaugural
from nltk.corpus import reuters
from nltk.corpus import stopwords
import pylab

english_stopwords = stopwords.words('english')


def get_frequency_distribution(words):
    fd = FreqDist(i.lower() for i in words)
    print(fd)
    sorted_fd = sorted(fd.values(), reverse=True)
    print(sorted_fd[0:10])
    return sorted_fd


def exclude_stopwords(words):
    return (i for i in words if i.lower() not in english_stopwords)


def main():
    # gutenberg
    gu_words = gutenberg.words()
    gu_words_exclude_stops = exclude_stopwords(gu_words)
    gu_fd1 = get_frequency_distribution(gu_words)
    gu_fd2 = get_frequency_distribution(gu_words_exclude_stops)

    pylab.plot(gu_fd1, color='red')
    pylab.plot(gu_fd2, color='orange')

    # inaugural
    in_words = inaugural.words()
    in_words_exclude_stops = exclude_stopwords(in_words)
    in_fd1 = get_frequency_distribution(in_words)
    in_fd2 = get_frequency_distribution(in_words_exclude_stops)

    pylab.plot(in_fd1, color='black')
    pylab.plot(in_fd2, color='gray')

    # reuters
    yen_words = reuters.words(categories='yen')
    yen_words_exclude_stops = exclude_stopwords(yen_words)
    yen_fd1 = get_frequency_distribution(yen_words)
    yen_fd2 = get_frequency_distribution(yen_words_exclude_stops)

    pylab.plot(yen_fd1, color='blue')
    pylab.plot(yen_fd2, color='green')

    pylab.xscale('log')
    pylab.yscale('log')
    pylab.show()


if __name__ == '__main__':
    main()
