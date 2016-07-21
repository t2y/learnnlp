# -*- coding: utf-8 -*-
from xml.etree import ElementTree

XML_FILE = 'hatebu.rdf'


def main():
    print('etree: reading from %s' % XML_FILE)

    with open(XML_FILE, 'r') as f:
        tree = ElementTree.parse(f)
        for i, item in enumerate(tree.iter(), 1):
            print('*' * 72)
            print('Element No. %d' % i)
            print('tag: %s' % item.tag)
            print('attribute: %s' % item.attrib)
            if item.text:
                if item.text.strip():
                    print('text:\n%s' % item.text)
                    print('-' * 72)
            print('*' * 72)
            print()


if __name__ == '__main__':
    main()
