import xml.etree.cElementTree as ET
import codecs
import json
import operator
from collections import defaultdict

filename = 'boston.osm'

def test(): 
    user_list = []
    user_dict = defaultdict(int)
    for _,element in ET.iterparse(filename):
        if 'user' in element.attrib:
            user_list.append(element.get('user'))
        else: 
            continue
    
    for item in user_list: 
        user_dict[item] +=1 
    sorted_user_dict = sorted(user_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
    pprint.pprint(sorted_user_dict)
    
    
if __name__ == "__main__":
    test()