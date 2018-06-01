#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re

"""Finds the tags

"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

problem = set()
other = set()
lower2 = set()
lower_colon2 = set()


def key_type(element, keys):

"""What type of key is this

Args:
    element(string): Element
    keys(string): keys
Returns:
    string: keys
"""
    if element.tag == "tag":
        key = element.attrib['k']
        if lower.search(key):
            keys['lower'] = keys.get('lower', 0) + 1
            lower2.add(key)
        elif lower_colon.search(key):
            keys['lower_colon'] = keys.get('lower_colon', 0) + 1
            lower_colon2.add(key)
        elif problemchars.search(key):
            keys['problemchars'] = keys.get('problemchars', 0) + 1
            problem.add(key)
        else:
            keys['other'] = keys.get('other', 0) + 1
            other.add(key)

    return keys


def process_map(filename):

"""Maps issues with elements

Args:
    filename(int): File that is queried
Returns:
    string: keys
"""
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


def test():

    keys = process_map(
        '/Users/ozgunbalaban/Dropbox/Programming/data/singapore.osm')
    pprint.pprint(keys)
    print(problem)
    print(other)
    print(lower2)
    print(lower_colon2)


if __name__ == "__main__":
    test()
