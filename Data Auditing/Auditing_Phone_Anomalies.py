import re
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict


filename = 'Boston.osm'
                
        
def read_file():
    for _, element in ET.iterparse(filename): 
        for child in element.getchildren(): 
            if child.tag=='tag': 
                key=child.get('k')
                if 'phone' in key: 
                    phone_number = child.get('v')
                    phone_set.add(phone_number)
    return phone_set
                

if __name__ == "__main__":
    street_types = defaultdict(set)
    phone_set = set()
    read_key = read_file()
    print len(read_key)
    print read_key
