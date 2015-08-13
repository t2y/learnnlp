# -*- coding: utf-8 -*-
import random

import pylab

from practice23_a import get_frequency_distribution

CHAR_NUM_LIMIT = 15
ORIGIN_WORDS = 'abcdefg'


def generate_words(num):
    for _ in xrange(num):
        yield ''.join(i for _ in xrange(random.randint(1, CHAR_NUM_LIMIT))
                      for i in random.choice(ORIGIN_WORDS))


def main():
    fd1 = get_frequency_distribution(generate_words(10000))
    pylab.plot(fd1, color='blue')

    fd2 = get_frequency_distribution(generate_words(1000000))
    pylab.plot(fd2, color='green')

    pylab.xscale('log')
    pylab.yscale('log')
    pylab.show()


if __name__ == '__main__':
    main()
