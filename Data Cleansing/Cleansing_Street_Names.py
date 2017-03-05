import re
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Heights", "North", "East", "West", "South"]

mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road", 
            "Ave": "Avenue", 
            "Ave.": "Avenue", 
            "St": "Street", 
            "St,": "Street", 
           "St.": "Street", 
           "ST": "Street"
            }


filename = 'boston.osm'
                
def process_addressanomalies(addressvalue): 
    match = street_type_re.search(addressvalue)
    if match: 
        street_type = match.group()
        if street_type not in expected: 
            street_types[street_type].add(addressvalue)

def update_name(): 
    for k, v in read_key.iteritems(): 
        for vitem in v: 
            match = street_type_re.search(vitem) 
            val =  match.group(0)
            if val in mapping: 
                new_name = vitem.replace(match.group(0), mapping[match.group(0)])
                print vitem, "==>", new_name
            

def read_file():
    for _, element in ET.iterparse(filename): 
        if element.tag == 'tag': 
            key=element.get('k')
            if 'addr:street' in key:
                addr_value = element.get('v')
                process_addressanomalies(addr_value)
    return street_types                

if __name__ == "__main__":
    street_types = defaultdict(set)
    read_key = read_file()
    better_adress = update_name()