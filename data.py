#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

"""
This file uses the example provided in the Nanodegree, but some of it is
changed to accommodate purposes outside this course.

So in the assignment I am asked to ignore tags other than node and way, but
I still want to keep them for other purposes. That is why they are not removed.

This code parses an OSM file that has nodes, ways and relations and creates
a json file so that it can be imported into MongoDB

This code is different from the one discussed in the nanodegree as I wanted
to do data wrangling in the database.

- I dont care about the problematic character as I did this analysis and there
  wasnt any
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospatial indexing. Make sure the values inside "pos" array are floats
      and not strings.

- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"


- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


# Mapping table provinding mapping from abbreviated street name to full name
mapping = {"St": "Street",
           "St.": "Street",
           "Ave": "Avenue",
           "Ave.": "Avenue",
           "Rd": "Road",
           "Rd.": "Road",
           "St": "Street",
           "St.": "Street",
           "rd": "Road",
           "garden": "Garden",
           "park": "Park",
           "road": "Road",
           "drive": "Drive"
           }

malay_mapping = {"Jl": "Jalan",
           "Jl.": "Jalan",
           "jalan": "Jalan",
           "Jln.": "Jalan",
           "jln": "Jalan"
           }

def shape_element(element):

    """ Creates shape elements such as nodes
    Args:
        element(string): Element
    Returns:
        string: node
    """
    node = {}


    if element.tag == "node" or element.tag == "way":
        node["type"] = element.tag
        created = {}


        # created
        for k, v in element.attrib.items():
            if k in CREATED:
                created[k] = v
            elif k != "lat" and k != "lon":
                node[k] = v
        node["created"] = created


        # Lat and lon under position
        if ("lat" in element.attrib):
            node["pos"] = [float(element.attrib["lat"]),
                           float(element.attrib["lon"])]

        # address related info
        address = {}
        for e in element.iter("tag"):

            if e.attrib["k"].startswith("addr:"):
                address[e.attrib["k"]] = e.attrib["v"]
            else:
                node[e.attrib["k"]] = e.attrib["v"]



            # node references
        if element.tag == "way":
            node_refs = []
            for e in element.iter("nd"):
                node_refs.append(e.attrib["ref"])
            if node_refs != []:
                node["node_refs"] = node_refs

        # if address exist
        if len(address) > 0:
            node['address'] = address

            # update street name
            if 'addr:street' in node['address']:
                node['address']['addr:street'] = update_name(
                    node['address']['addr:street'], mapping)

                node['address']['addr:street'] = update_malay_name(
                    node['address']['addr:street'], malay_mapping)

            # delete postcodes that are less than 5 digits
            if 'addr:postcode' in node['address']:
                if len(node['address']['addr:postcode']) < 5:
                    node['address'].pop('addr:postcode')


        return node
    else:
        return None


def update_name(name, mapping):

    """ Updates street names that are in English such as Road
    Args:
        name(string): name
        mapping(List): mapping list
    Returns:
        string: name
    """

    # For English names check last word
    last_word = name.rsplit(None, 1)[-1]
    if last_word in mapping:
        name = name.rsplit(' ', 1)[0] + ' ' + mapping[last_word]
    print name   # debugging
    return name

def update_malay_name(name, mapping):

    """ Updates street names that are in Malay such as Jalan
    Args:
        name(string): name
        malay_mapping(List): mapping list
    Returns:
        string: name
    """

    # For Malay names check first word
    first_word = name.rsplit()[0]
    if first_word in mapping:
        name = mapping[first_word] + ' ' + name.rsplit(' ', 1)[-1]

    return name

def process_map(file_in, pretty=False):

   # Change this file for output file

    file_out = "singapore.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def test():
    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.

    # change this for input osm file

    process_map(('singapore.osm'), False)
    # pprint.pprint(data)



if __name__ == "__main__":
    test()
