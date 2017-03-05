import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict

filename = 'boston.osm'

def test(): 
    users = set()
    for _,element in ET.iterparse(filename):
        if 'user' in element.attrib:
            users.add(element.get('user'))
    print len(users)
    users_list = list(users)
    print "Printing List of ten Unique Users:", users_list[:10]
    
if __name__ == "__main__":
    test()