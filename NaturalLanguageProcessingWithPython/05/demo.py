# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import brown

brown_tagged_sents = brown.tagged_sents(categories='news')
brown_sents = brown.sents(categories='news')

default_tagger = nltk.DefaultTagger('NN')
print(default_tagger.tag(brown_sents[2007]))
r = default_tagger.evaluate(brown_tagged_sents)
print(r)

unigram_tagger = nltk.UnigramTagger(brown_tagged_sents, verbose=True)
print(unigram_tagger.tag(brown_sents[2007]))
r = unigram_tagger.evaluate(brown_tagged_sents)
print(r)

train_size = int(len(brown_tagged_sents) * 0.9)
print(train_size)
train_sents = brown_tagged_sents[:train_size]
test_sents = brown_tagged_sents[train_size:]

unigram_tagger = nltk.UnigramTagger(train_sents, verbose=True)
print(unigram_tagger.tag(brown_sents[2007]))
r = unigram_tagger.evaluate(test_sents)
print(r)

t0 = nltk.DefaultTagger('NN')
t1 = nltk.UnigramTagger(train_sents, backoff=t0, verbose=True)
t2 = nltk.BigramTagger(train_sents, backoff=t1, verbose=True)
r = t2.evaluate(test_sents)

t22 = nltk.BigramTagger(train_sents, cutoff=2, backoff=t1, verbose=True)
r = t22.evaluate(test_sents)
print(r)

t3 = nltk.TrigramTagger(train_sents, backoff=t2, verbose=True)
r = t3.evaluate(test_sents)
print(r)
