#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Count the number of tags
"""
import xml.etree.cElementTree as ET
import pprint


def count_tags(filename):
    tags = {}

    for event, elem in ET.iterparse(filename, events=('start',)):
        tags[elem.tag] = tags.get(elem.tag, 0) + 1
    return tags


def test():
    tags = count_tags(
        '/Users/ozgunbalaban/Dropbox/Programming/data/singapore.osm')
    pprint.pprint(tags)


if __name__ == "__main__":
    test()
