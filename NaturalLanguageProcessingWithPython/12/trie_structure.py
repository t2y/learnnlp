# -*- coding: utf-8 -*-
"""
https://ja.wikipedia.org/wiki/トライ木

"""
from pprint import pprint

import nltk


DICT_ENTRIES = [
    [u"かれ", {'pos':'V-Y', 'lemma':u"枯れ"}],
    [u"かれ", {'pos':'V-Z', 'lemma':u"枯れ"}],
    [u"かれ", {'pos':'N', 'lemma':u"彼"}],
    [u"の", {'pos':'J-K', 'lemma':u"の"}],
    [u"く", {'pos':'N', 'lemma':u"区"}],
    [u"くる", {'pos':'V-S', 'lemma':u"来る"}],
    [u"くる", {'pos':'V-T', 'lemma':u"来る"}],
    [u"くるま", {'pos':'N', 'lemma':u"車"}],
    [u"ま", {'pos':'N', 'lemma':u"間"}],
    [u"まで", {'pos':'J-F', 'lemma':u"まで"}],
    [u"で", {'pos':'J-K', 'lemma':u"で"}],
    [u"でま", {'pos':'N', 'lemma':u"デマ"}],
    [u"まつ", {'pos':'N', 'lemma':u"松"}],
    [u"まつ", {'pos':'V-S', 'lemma':u"待つ"}],
    [u"まつ", {'pos':'V-T', 'lemma':u"待つ"}],
    [u"つ", {'pos':'N', 'lemma':u"津"}]
]


def insert(trie, key, value):
    """
    >>> from pprint import pprint
    >>> trie = {}

    >>> insert(trie, 'test', 'data')
    >>> trie
    {'t': {'e': {'s': {'t': {'value': ['data']}}}}}

    >>> insert(trie, 'text', 'string')
    >>> pprint(trie)
    {'t': {'e': {'s': {'t': {'value': ['data']}},
                 'x': {'t': {'value': ['string']}}}}}

    >>> insert(trie, 'tmp', 'file')
    >>> pprint(trie)
    {'t': {'e': {'s': {'t': {'value': ['data']}},
                 'x': {'t': {'value': ['string']}}},
           'm': {'p': {'value': ['file']}}}}
    """
    if key:
        first, rest = key[0], key[1:]
        if first not in trie:
            trie[first] = {}
        insert(trie[first], rest, value)
    else:
        if not 'value' in trie:
            trie['value'] = []
        trie['value'].append(value)


def common_prefix_search(trie, key):
    """
    >>> from pprint import pprint
    >>> data = {
    ...     'test': 'data',
    ...     'text': 'string',
    ...     'tmp': 'file',
    ... }
    >>> trie = {}
    >>> for key, value in data.items():
    ...     insert(trie, key, value)
    >>> common_prefix_search(trie, 'test')
    ['data']
    >>> common_prefix_search(trie, 'tmp')
    ['file']
    """
    ret = []
    if 'value' in trie:
        ret += trie['value']

    if key:
        first, rest = key[0], key[1:]
        if first in trie:
            ret += common_prefix_search(trie[first], rest)

    return ret


def is_connectable(bnode, cnode):
    """
    >>> bnode = {'entry': {'pos': 'N'}}
    >>> cnode = {'entry': {'pos': 'J-K'}}
    >>> is_connectable(bnode, cnode)
    True
    >>> bnode = {'entry': {'pos': 'V-Y'}}
    >>> cnode = {'entry': {'pos': 'V-S'}}
    >>> is_connectable(bnode, cnode)
    False
    """
    ctable = set([
        ('BOS', 'N'), ('BOS', 'V'), ('BOS', 'T'),
        ('T', 'N'), ('N', 'J'), ('J', 'N'), ('J', 'V'),
        ('V-T', 'N'), ('V-T', 'J-F'), ('V-Y', 'A'),
        ('V-S', 'EOS'), ('A', 'EOS'),
    ])
    bpos = bnode['entry']['pos']
    bpos_s = bpos.split('-')[0]
    cpos = cnode['entry']['pos']
    cpos_s = cpos.split('-')[0]
    return (((bpos, cpos) in ctable) or
            ((bpos_s, cpos) in ctable) or
            ((bpos, cpos_s) in ctable) or
            ((bpos_s, cpos_s) in ctable))


_BOS_ENTRY = {'pos':'BOS','lemma':u'BOS','length':1}
_EOS_ENTRY = {'pos':'EOS','lemma':u'EOS','length':1}


def enum_solutions(node):
    """
    >>> node = {'entry': {'lemma': u'EOS'}}
    >>> enum_solutions(node)
    [[u'EOS']]

    >>> node = {
    ...     'entry': {'lemma': u'これ'},
    ...     'next': [
    ...         {
    ...             'entry': {'lemma': u'は'},
    ...             'next': [
    ...                 {
    ...                     'entry': {'lemma': u'テスト'},
    ...                     'next': [
    ...                         {
    ...                             'entry': {'lemma': u'EOS'},
    ...                             'next': [],
    ...                         },
    ...                     ],
    ...                 }
    ...             ]
    ...         }
    ...     ]
    ... }
    >>> enum_solutions(node)
    [[u'\xe3\x81\x93\xe3\x82\x8c', u'\xe3\x81\xaf', u'\xe3\x83\x86\xe3\x82\xb9\xe3\x83\x88', u'EOS']]
    """
    results = []
    if node['entry']['lemma'] == u'EOS':
        return [[u'EOS']]

    for nnode in node['next']:
        for solution in enum_solutions(nnode):
            results.append([node['entry']['lemma']] + solution)

    return results


def analyze_simple(trie, sent, connect_func=lambda x, y: True):
    """
    trie 構造から形態素が接続できるかどうかで node を作成し、
    作成した node から形態素の接続可能なすべての組み合わせを返す
    """
    bos_node = {'next':[], 'entry': _BOS_ENTRY}  # ... (1)
    end_node_list = nltk.defaultdict(list)  # ... (2)
    end_node_list[0].append(bos_node)
    for i in range(0, len(sent)+1):  # ... (6)
        if i < len(sent):
            cps_results = common_prefix_search(trie, sent[i:].encode('utf-8'))
        else:
            # EOS
            cps_results = [_EOS_ENTRY]

        for centry in cps_results:
            cnode = {'next': [], 'entry': centry}
            for bnode in end_node_list[i]:
                if connect_func(bnode, cnode):  # ... (3)
                    bnode['next'].append(cnode)  # ... (5)
                    end_nodes = end_node_list[i+centry['length']]
                    if not cnode in end_nodes:
                        end_nodes.append(cnode)  # ... (4)

    print('-' * 72)
    pprint(bos_node)
    print('-' * 72)
    return enum_solutions(bos_node)  # ... (7)


def main():
    matrie = {}
    for entry in DICT_ENTRIES:
        entry[1]['length'] = len(entry[0])
        insert(matrie, entry[0].encode('utf-8'), entry[1])

    res = analyze_simple(matrie, u"かれのくるまでまつ", is_connectable)
    print('\n'.join('/'.join(sent) for sent in res))


if __name__ == '__main__':
    main()
