#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re

"""

"""


def get_user(element):
    user = None
    if element.tag == "node" or element.tag == "way" or element.tag == "relation":
        user = element.attrib["uid"]

    return user


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if get_user(element) != None:
            users.add(get_user(element))

    return users


def test():
    users = process_map('/Users/ozgunbalaban/Dropbox/Programming/data/singapore.osm')
    pprint.pprint(users)
    print (len(users))


if __name__ == "__main__":
    test()