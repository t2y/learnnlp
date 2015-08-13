# -*- coding: utf-8 -*-
from __future__ import print_function
from nltk.text import Text

Text._COPY_TOKENS = False

# from nltk.book import *
from nltk.book import text2


def main():
    print('*' * 72)
    print('from here ')
    print(text2)

    # show text2 length 
    print(len(text2))

    # unique
    s2 = set(text2)
    print(len(s2))

    # groupby, a little tricky
    from itertools import groupby
    g2 = [(key, len(list(i))) for key, i in groupby(sorted(text2))]
    print(g2[1000:1010])

    # readability, pythonic
    d = {}
    for word in text2:
        if d.get(word) is None:
            d[word] = 1
        else:
            d[word] += 1
    print(d['amusement'])

    # verify
    print(len(list(i for i in text2 if i == 'amusement')))

    # use default dict, more pythonic
    from collections import defaultdict
    #d = defaultdict(int)
    d = defaultdict(lambda: 0)
    for word in text2:
        d[word] += 1
    print(d['amusement'])

    # use standard library, excellent!
    from collections import Counter
    c = Counter(text2)
    print(c['amusement'])


if __name__ == '__main__':
    main()
