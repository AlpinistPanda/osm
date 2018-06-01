import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "singapore.osm"

# Regex for abbreviated street names
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


# Common street names we may find
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
            "View", "Walk", "Way", "Square", "Lane", "Road", "Link", "Loop",
            "Park", "Rise", "Terrace",
            "Trail", "Parkway", "Commons"]

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


def audit_street_type(street_types, street_name):

    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        # We will like to only examine the streets which are unusual/abbreviated
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    """Checks if it is a street
    Args:
        elem(string): Element
    Returns:
        string: Element
    """
    return (elem.attrib['k'] == "addr:street")


def is_zip_code(elem):
    """Checks if it is a zip code
    Args:
        elem(string): Zip code element
    Returns:
        string: Element
    """
    return (elem.attrib['k'] == "addr:postcode")

# Audit given file, returning a possible street types set which may need to examine/fix


def audit(osmfile):
    """Corrects the xml file

    Args:
        osmfile(int): Osm file
    Returns:
        string: street type
    """
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    postcodes = defaultdict(set)

    # As the given file can be quite large, we process it iteratively
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        # Audit only street data
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping, st_type):
    """Fix street name
    Args:
        name(string): name of the street
        mapping(string): mapping
        st_type(string): street type
    Returns:
        string: Explanation of returned parameter.
    """

# Looking into our mapping table to find possible fixed name
    if st_type in mapping:
        name = street_type_re.sub(mapping[st_type], name)

    return name

#


def audit_fix():
    """Audit and fix the street names
    """
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    logFile = open('street.txt', 'w')
    # newOsm = open('newsg.osm', 'w')
    pprint.pprint(dict(st_types), logFile)

    # osm_file = open(osmfile, "r")

    # For each possible problematic street name fix it if we can
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping, st_type)
            if name != better_name:
                print name, "=>", better_name

    osm_file = open(OSMFILE, "r")
    # As the given file can be quite large, we process it iteratively
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        # Audit only street data
        if elem.tag == "node" or elem.tag == "way":
            for key, tag in elem.iter("tag"):
                if is_street_name(tag):
                    print(elem.tag[key].attrib['v'])
                    tag.attrib['v'] = update_name(
                        tag.attrib['v'], mapping, st_type)


if __name__ == '__main__':
    audit_fix()
