# -*- coding: utf-8 -*-
from __future__ import print_function 

"""
trie データ構造の pure Python 実装

* http://pythonhosted.org/PyTrie/
"""


def sample():
    """
    >>> from pytrie import SortedStringTrie as trie
    >>> t = trie(an=0, ant=1, all=2, allot=3, alloy=4, aloe=5, are=6, be=7)
    >>> t
    SortedStringTrie({'all': 2, 'allot': 3, 'alloy': 4, 'aloe': 5, 'an': 0, 'ant': 1, 'are': 6, 'be': 7})
    >>> t.keys(prefix='al')
    ['all', 'allot', 'alloy', 'aloe']
    >>> t.items(prefix='an')
    [('an', 0), ('ant', 1)]
    >>> t.longest_prefix('antonym')
    'ant'
    >>> t.longest_prefix_item('allstar')
    ('all', 2)
    >>> t.longest_prefix_value('area', default='N/A')
    6
    >>> t.longest_prefix('alsa')
    Traceback (most recent call last):
    ...
    KeyError
    >>> t.longest_prefix_value('alsa', default=-1)
    -1
    >>> list(t.iter_prefixes('allotment'))
    ['all', 'allot']
    >>> list(t.iter_prefix_items('antonym'))
    [('an', 0), ('ant', 1)]
    """
