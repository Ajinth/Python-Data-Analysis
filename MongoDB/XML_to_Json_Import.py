import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import sys
sys.setrecursionlimit(10000)
from collections import defaultdict

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


'''Parameters for Zipcode Clean Up'''

zipcheckalpha = re.compile(r'[a-zA-Z].*')
zipcheckhyphen = re.compile(r'^(\d{5})-\d{4}$')


'''Parameters for Address Street Name Clean Up'''

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


'''Parameters for Phone Clean Up'''

# Regular Expression to check whether the phone number is starting with + 1 
phonecheckone = re.compile(r'^\+[1]\s*')

# Regular Expression to check whether the phone number has a hyphen in it 
phonecheckhyphen = re.compile(r'\-+')

# Regular Expression to check whether the phone number has any white spaces in it 
phonecheckspace = re.compile(r'\s+?')

# Regular Expression to check whether the phone number contains any parenthesis
phonecheckpar1 = re.compile(r'\(+')
phonecheckpar2 = re.compile(r'\)+')

# Regular Expression to check whether the phone number contains any periods
phonecheckperiod = re.compile(r'\.+')

# Regular Expression to check whether the phone number contains any alphabets in them 
phonecheckalpha = re.compile(r'[a-zA-Z].*')

# Regular Expression to check whether the phone number has any commas in it 
phonecheckcomma = re.compile(r'\,+')

#-------------------------------------------------------------------------------------------

'''Cleansing Function to Clean Zipcodes'''

def clean_zipcode(zipcode):
    ca = clean_zalpha(zipcode)
    if ca:
        return zipcode 
    else: 
        cleaned_zipcode = clean_zhyphen(zipcode)
        return cleaned_zipcode 


def clean_zalpha(zipcode): 
    match = zipcheckalpha.search(zipcode)
    if match: 
        return zipcode 
    else: 
        pass
            

def clean_zhyphen(zipcode): 
    match = phonecheckhyphen.search(zipcode)
    if match: 
        zipcode = match.group(0).split('-')[0]
        return zipcode
    else: 
        return zipcode

#-------------------------------------------------------------------------------------------


'''Cleansing Function to Clean Street Names'''

def clean_streetname(old_name): 
    match = street_type_re.search(old_name) 
    val =  match.group(0)
    if val in mapping: 
        name = old_name.replace(match.group(0), mapping[match.group(0)])
        return name
    else:
        name = old_name
        return name
#-------------------------------------------------------------------------------------------

    
'''Cleansing Function to Clean Phone Numbers'''

def clean_phone(phone):
    ca = clean_alpha(phone)
    if ca:
        return phone 
    else: 
        whitespace= clean_whitespaces(phone) 
        hyphen= clean_hyphen(whitespace)
        plusone=clean_plusone(hyphen)
        paren1=clean_paranthesis1(plusone)
        paren2= clean_paranthesis2(paren1)
        prd= clean_period(paren2)
        cleanone = clean_one(prd)
        cleancomma = clean_comma(cleanone)
        return cleancomma 


def clean_alpha(phone): 
    match = phonecheckalpha.search(phone)
    if match: 
        return phone 
    else: 
        pass
            
def clean_whitespaces(phone): 
    match=phonecheckspace.search(phone)
    if match: 
        phone=phone.replace(match.group(0), '')
        return phone
    else: 
        return phone


def clean_hyphen(phone): 
    match = phonecheckhyphen.search(phone)
    if match: 
        phone = phone.replace(match.group(0), '')
        return phone
    else: 
        return phone
        
def clean_plusone(phone): 
    match = phonecheckone.search(phone)
    if match: 
        phone = phone.replace(match.group(0), '')
        return phone
    else: 
        return phone 
        
def clean_paranthesis1(phone): 
    match = phonecheckpar1.search(phone)
    if match: 
        phone = phone.replace(match.group(0), '')
        return phone
    else: 
        return phone

def clean_paranthesis2(phone): 
    match = phonecheckpar2.search(phone)
    if match: 
        phone = phone.replace(match.group(0), '')
        return phone
    else: 
        return phone

        
def clean_period(phone): 
    match = phonecheckperiod.search(phone)
    if match: 
        phone = phone.replace(match.group(0), '')
        return phone
    else: 
        return phone
        
def clean_one(phone): 
    if phone.startswith('1') or phone.startswith('+'): 
        phone = phone[1:]
        return phone 
    else: 
        return phone 


def clean_comma(phone): 
    match = phonecheckcomma.search(phone)
    if match: 
        phone = phone.replace(match.group(0), '')
        return phone
    else: 
        return phone       
    
#-------------------------------------------------------------------------------------------
    
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
            
            '''Included the logic to clean the Phone Number by calling the Phone Cleaning Function prior to JSON Import'''
            if key == 'phone': 
                if len(clean_phone(child.get('v'))) == 10: 
                    node['phonenumber'] = clean_phone(child.get('v'))
                else: 
                    node['phonenumber'] = 'Phone Number Removed Due to Incorrect Value'
                    
            
            if key is not None: 
                if key.startswith('addr:'):
                    split_key = key.split(":")
                    
                    '''Included the logic to clean the Street Name and Post Codes by calling the respective functions
                    prior to JSON Import'''
                    
                    if split_key[1] == 'street': 
                        node['address'][split_key[1]]= clean_streetname(child.get('v'))
                    elif split_key[1] == 'postcode':
                        node['address'][split_key[1]]= clean_zipcode(child.get('v'))
                    else: 
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