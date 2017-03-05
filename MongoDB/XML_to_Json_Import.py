import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import sys
sys.setrecursionlimit(10000)
from collections import defaultdict


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def floatOrNofloat(n):
    return float(n) if n else None
    
def shape_element(element): 
    node = defaultdict(dict) 
    if element.tag == "node" or element.tag == "way":
        
        node["tag"] = element.tag

        node ["id"] = element.get('id')

        lat = element.get('lat')

        lon = element.get('lon')

        if lat or lon:
            node['pos'] = [floatOrNofloat(lat), floatOrNofloat(lon)]
        
        node["created"] = {}

        for key in CREATED:
            node["created"][key] = element.get(key)
        
        for child in element.getchildren():
            
            key = child.get("k")
            ref = child.get("ref")
            
            if key == 'address': 
                node['fulladdress'] = child.get('v')
            
            if key is not None: 
                if key.startswith('addr:'):
                    split_key = key.split(":")
                    node['address'][split_key[1]] = child.get('v')
                elif 'amenity' in key: 
                    node['amenity'] = child.get('v')
                elif 'name' in key: 
                    node['name'] = child.get('v')
            
            if ref: 
                if "node_refs" not in node: 
                    node["node_refs"] = []
                else: 
                    node["node_refs"].append(ref)
        
        return node
    else:
        return None
        

    
def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    data = process_map('Boston.osm', True)
    

if __name__ == "__main__":
    test()