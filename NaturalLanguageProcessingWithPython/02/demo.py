# -*- coding: utf-8 -*-
from nltk import FreqDist
from nltk.corpus import reuters


yen = reuters.words(categories='yen')
fd1 = FreqDist(i.lower() for i in yen)
sfd1 = sorted(fd1.values(), reverse=True)

# ---

for i, v in enumerate(fd1[0:100], 1): print('%d, %d, %d'  % (i, v, i*v))

# ---

import pylab
pylab.plot(sfd1, color='red')

pylab.xscale('log')
pylab.yscale('log')
pylab.show()

# ---

from nltk.corpus import stopwords
english_stopwords = stopwords.words('english')

yen_exclude_stops = [i for i in yen if i.lower() not in english_stopwords]
fd2 = FreqDist(i.lower() for i in yen_exclude_stops)
sfd2 = sorted(fd2.values(), reverse=True)

pylab.plot(sfd1, color='red')
pylab.plot(sfd2, color='orange')
pylab.show()
