# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import brown


def gender_features(word):  # 素性抽出関数
    """
    >>> gender_features('Shrek')  # feature: 素性 -> 符号化
    {'last_letter': 'k'}
    """
    return {'last_letter': word[-1]}


import nltk
from nltk import NaiveBayesClassifier
from nltk.corpus import names
import random

names = ([(name, 'male') for name in names.words('male.txt')] +
         [(name, 'female') for name in names.words('female.txt')])
random.shuffle(names)
print(names[:3])

feature_sets = [(gender_features(n), g) for (n, g) in names]
print(feature_sets[:3])
train_set, test_set = feature_sets[500:], feature_sets[:500]

classifier = NaiveBayesClassifier.train(train_set)
print(classifier.classify(gender_features('Neo')))
print(classifier.classify(gender_features('Trinity')))
print(nltk.classify.accuracy(classifier, test_set))
print(classifier.show_most_informative_features(5))

from nltk.classify import apply_features
train_set = apply_features(gender_features, names[500:])
test_set = apply_features(gender_features, names[:500])

from collections import OrderedDict
from string import ascii_lowercase

def gender_features2(name):
    """
    >>> gender_features2('Shrek')  # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('firstletter', 's'), ('lastletter', 'k'),
    ('count(a)', 0), ('has(a)', False), ('count(b)', 0), ('has(b)', False),
    ('count(c)', 0), ('has(c)', False), ('count(d)', 0), ('has(d)', False),
    ('count(e)', 1), ('has(e)', True), ('count(f)', 0), ('has(f)', False),
    ('count(g)', 0), ('has(g)', False), ('count(h)', 1), ('has(h)', True),
    ('count(i)', 0), ('has(i)', False), ('count(j)', 0), ('has(j)', False),
    ('count(k)', 1), ('has(k)', True), ('count(l)', 0), ('has(l)', False),
    ('count(m)', 0), ('has(m)', False), ('count(n)', 0), ('has(n)', False),
    ('count(o)', 0), ('has(o)', False), ('count(p)', 0), ('has(p)', False),
    ('count(q)', 0), ('has(q)', False), ('count(r)', 1), ('has(r)', True),
    ('count(s)', 1), ('has(s)', True), ('count(t)', 0), ('has(t)', False),
    ('count(u)', 0), ('has(u)', False), ('count(v)', 0), ('has(v)', False),
    ('count(w)', 0), ('has(w)', False), ('count(x)', 0), ('has(x)', False),
    ('count(y)', 0), ('has(y)', False), ('count(z)', 0), ('has(z)', False)])
    """
    features = OrderedDict()
    features['firstletter'] = name[0].lower()
    features['lastletter'] = name[-1].lower()
    for letter in ascii_lowercase:
        features['count(%s)' % letter] = name.lower().count(letter)
        features['has(%s)' % letter] = letter in name.lower()
    return features

feature_sets2 = [(gender_features2(n), g) for (n, g) in names]
train_set, test_set = feature_sets2[500:], feature_sets2[:500]
classifier = NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))


train_names = names[1500:]
devtest_names = names[500:1500]
test_names = names[:500]

train_set = [(gender_features(n), g) for (n, g) in train_names]
devtest_set = [(gender_features(n), g) for (n, g) in devtest_names]
test_set = [(gender_features(n), g) for (n, g) in test_names]
classifier = NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))

errors = []
for (name, tag) in devtest_names:
    guess = classifier.classify(gender_features(name))
    if guess != tag:
        errors.append((tag, guess, name))
print(errors[:10])

def gender_features3(word):
    """
    >>> gender_features3('Shrek')
    {'suffix2': 'ek', 'suffix1': 'k'}
    """
    return {'suffix1': word[-1:], 'suffix2': word[-2:]}

train_set = [(gender_features3(n), g) for (n, g) in train_names]
devtest_set = [(gender_features3(n), g) for (n, g) in devtest_names]
test_set = [(gender_features3(n), g) for (n, g) in test_names]
classifier = NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))



#brown_tagged_sents = brown.tagged_sents(categories='news')
#brown_sents = brown.sents(categories='news')
#
#default_tagger = nltk.DefaultTagger('NN')
#print(default_tagger.tag(brown_sents[2007]))
#r = default_tagger.evaluate(brown_tagged_sents)
#print(r)
#
#unigram_tagger = nltk.UnigramTagger(brown_tagged_sents, verbose=True)
#print(unigram_tagger.tag(brown_sents[2007]))
#r = unigram_tagger.evaluate(brown_tagged_sents)
#print(r)
#
#train_size = int(len(brown_tagged_sents) * 0.9)
#print(train_size)
#train_sents = brown_tagged_sents[:train_size]
#test_sents = brown_tagged_sents[train_size:]
#
#unigram_tagger = nltk.UnigramTagger(train_sents, verbose=True)
#print(unigram_tagger.tag(brown_sents[2007]))
#r = unigram_tagger.evaluate(test_sents)
#print(r)
#
#t0 = nltk.DefaultTagger('NN')
#t1 = nltk.UnigramTagger(train_sents, backoff=t0, verbose=True)
#t2 = nltk.BigramTagger(train_sents, backoff=t1, verbose=True)
#r = t2.evaluate(test_sents)
#
#t22 = nltk.BigramTagger(train_sents, cutoff=2, backoff=t1, verbose=True)
#r = t22.evaluate(test_sents)
#print(r)
#
#t3 = nltk.TrigramTagger(train_sents, backoff=t2, verbose=True)
#r = t3.evaluate(test_sents)
#print(r)
