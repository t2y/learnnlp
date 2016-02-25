# -*- coding: utf-8 -*-
from __future__ import print_function

import sys

from janome.tokenizer import Tokenizer


tokenizer = Tokenizer()


def filter_word_class(text, word_classes=['名詞']):
    d = {}
    for i, token in enumerate(tokenizer.tokenize(text)):
        word_class = token.part_of_speech.split(',')[0]
        if isinstance(word_class, unicode):
            word_class = word_class.encode('utf-8')

        if word_class in word_classes:
            if d.get(token.surface) is None:
                d[token.surface] = {
                    'term': token.surface,
                    'positions': [i],
                    'word_class': word_class.decode('utf-8'),
                }
            else:
                d[token.surface]['positions'].append(i)
    return d


def filter_nouns(tokens, word_info):
    return [i for i in tokens if word_info.get(i) is not None]


def get_noun_chunk(tokens, word_info):
    def is_continus_position(prev_positions, cur_positions):
        for pos in map(lambda x: x - 1, cur_positions):
            if pos in prev_positions:
                return True
        return False

    l = []
    cur_index = 0
    prev = word_info.get(tokens[0])
    if prev is not None:
        l.append(prev['term'])

    for token in tokens[1:]:
        info = word_info.get(token)
        if info is not None:
            if prev is not None:
                if is_continus_position(prev['positions'], info['positions']):
                    l[cur_index] += info['term']
                else:
                    phrase = prev['term'] + info['term']
                    l.append(phrase)
                    cur_index += 1
            else:
                l.append(info['term'])
                cur_index += 1
        else:
            l.append(token)
            cur_index += 1

        prev = info
    return l


def get_token_with_class(text):
    l = []
    for token in tokenizer.tokenize(text):
        word_class = token.part_of_speech.split(',')[0]
        if isinstance(word_class, str):
            word_class = word_class.decode('utf-8')
        s = u'(' + token.surface + u': ' + word_class + u')'
        l.append(s)
    return l


def get_token(text):
    return [token.surface for token in tokenizer.tokenize(text)]


def print_str(s, header):
    print(header.encode('utf-8'))
    print('=' * 32)
    print(s.encode('utf-8'))
    print('\n')


def print_element(tokens, header):
    print(header.encode('utf-8'))
    print('=' * 32)
    print(u'  '.join(i for i in tokens).encode('utf-8'))
    print('\n')


def main(text=None):
    if text is None:
        if len(sys.argv) < 2:
            print('usage: python chunk_noun_phrase.py text')
            sys.exit(0)
        text = sys.argv[1].decode('utf-8')

    print_str(text, u'オリジナルのテキスト')
    print_element(get_token_with_class(text), u'通常の形態素解析 by janome')

    # morphological analysis
    tokens = get_token(text)

    # retrieve noun words
    word_info = filter_word_class(text)
    noun_tokens = filter_nouns(tokens, word_info)
    print_element(noun_tokens, u'名詞のみを取り出したトークン列')

    # retrieve noun phrase
    noun_chunks = get_noun_chunk(tokens, word_info)
    print_element(noun_chunks, u'名詞句のみでチャンク処理')


if __name__ == '__main__':
    main()
