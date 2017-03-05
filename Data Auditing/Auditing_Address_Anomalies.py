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


filename = 'boston.osm'
                
def process_addressanomalies(addressvalue): 
    match = street_type_re.search(addressvalue)
    if match: 
        street_type = match.group()
        if street_type not in expected: 
            street_types[street_type].add(addressvalue)
        
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
pprint.pprint(dict(read_key))

    
