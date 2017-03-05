import re
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

filename = 'boston.osm'


def process_address(addr_value):
    if re.search(lower,addr_value):
        keys['lower'] += 1
    elif re.search(lower_colon, addr_value): 
        keys['lower_colon'] += 1
    elif re.search(problemchars, addr_value): 
        keys['problemchars'] += 1 
    else: 
        keys['other'] += 1
                

def read_file():
    for _, element in ET.iterparse(filename): 
        if element.tag == 'tag': 
            key=element.get('k')
            if 'addr:' in key:
                addr_value = element.get('v')
                process_address(addr_value)
    return keys
                    

if __name__ == "__main__":
    keys = defaultdict(int)
    read_key = read_file()
    print read_key
