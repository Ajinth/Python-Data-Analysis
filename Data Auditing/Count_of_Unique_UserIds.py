import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict

filename = 'boston.osm'

def test(): 
    tag_list = []
    tag_dict = defaultdict(int)
    for _, element in ET.iterparse(filename): 
        tag_list.append(element.tag)
    for item in tag_list: 
        tag_dict[item] += 1
    pprint.pprint(tag_dict)


if __name__ == "__main__":
    test()