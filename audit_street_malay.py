""" Changes for Malay street names

"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "singapore.osm"


# Regex for abbreviated street names that are in the front
street_type_malay_re = re.compile(r'^[a-zA-Z0-9]+\.*', re.IGNORECASE)

# Common street names we may find
expected = ["Jalan", "Lorong", "Taman", "Lengkong"]


# Mapping table provinding mapping from abbreviated street name to full name
mapping = {"Jl": "Jalan",
           "Jl.": "Jalan",
           "jalan": "Jalan",
           "Jln.": "Jalan",
           "jln": "Jalan"
           }


# Bucket our street adresses by street names
def audit_street_type(street_types, street_name):
    """Bucket our street adresses by street names
    Args:
        street_types(int): Explanation of param_1.
        street_name(string): Explanation of param_2.
    """
    m = street_type_malay_re.search(street_name)
    if m:
        street_type = m.group()
        # We will like to only examine the streets which are unusual/abbreviated
        if street_type not in expected:
            street_types[street_type].add(street_name)


# Is street
def is_street_name(elem):
    """Is street

    Args:
        element(string): Element
    Returns:
        string: Element
    """
    return (elem.attrib['k'] == "addr:street")

# Audit given file, returning a possible street types set which may need to examine/fix


def audit(osmfile):
    """Check and correct osm file

    Args:
        osm_file(string): osm file

    Returns:
        string: Street types
    """
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)

    # As the given file can be quite large, we process it iteratively
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        # Audit only street data
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


#
def update_name(name, mapping, st_type):


    """Fix the street name if we can
    Args:
        name(string): name of the street
        mapping(string): mapping
        st_type(string): type of the street
    Returns:
        string: Name
    """

# Looking into our mapping table to find possible fixed name
    if st_type in mapping:
        name = street_type_malay_re.sub(mapping[st_type], name)

    return name


def audit_fix():
    """Audit and fix the street names

    """
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    logFile = open('malay_street.txt', 'w')
    pprint.pprint(dict(st_types), logFile)

    # For each possible problematic street name fix it if we can
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping, st_type)
            if name != better_name:
                print name, "=>", better_name


if __name__ == '__main__':
    audit_fix()
