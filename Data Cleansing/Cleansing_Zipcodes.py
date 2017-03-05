# Importing all the Needed Libraries
import re
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict


# Regular Expression to check whether the phone number contains any alphabets in them 
zipcheckalpha = re.compile(r'[a-zA-Z].*')
zipcheckhyphen = re.compile(r'\-+')

def identifypostcode(): 
    
    '''Identifying Post Codes that have Characters 
        in them and sending them in a manual review list'''
    
    for zip_item in read_key:
        match=zipcheckalpha.search(zip_item)
        if match: 
            zipmanual.append("To be Review Manually:" + zip_item)
        else:
            zipauto.append(zip_item)

def fixpostcode(): 
    
    '''Check for Hyphens in Post Code and Extract the first part of the Zipcode''' 
    
    for zipcode_item in zipauto: 
        match = zipcheckhyphen.search(zipcode_item)
        if match: 
            ziphyphen.append(zipcode_item)
            zipcode_split = zipcode_item.split('-')
            ziphyphencleaned.append(zipcode_split[0]) 
        else: 
            ziphyphencleaned.append(zipcode_item)
        

            
def read_file():
    for _, element in ET.iterparse(filename): 
        for child in element.getchildren(): 
            if child.tag=='tag': 
                key=child.get('k')
                if 'addr:postcode' in key: 
                    post_code = child.get('v')
                    postcode.append(post_code)
    return postcode


    

if __name__ == "__main__":
    count = 0 
    
    '''Initializing the different list before using them through the 
    different steps of the cleanse process with the regular expression'''
    
    
    postcode = []
    zipmanual=[]
    ziphyphen=[]
    ziphyphencleaned=[]
    zipauto=[]
    
    read_key = read_file()
    identifypostcode = identifypostcode()
    fixpostcode=fixpostcode()
    
    print "Zip Code Cleansing High Level Stats"
    print "---------------------------------------------------------------------"
    print "Total Number of Zip Codes Encountered in the File: ", len(read_key)
    print "Total Number of Zip Codes to be Cleaned Manually: ", len(zipmanual)
    print "Total Number of Zip Codes Cleaned Using Regular Expressions: ", len(zipauto)
    print "Total Number of Zip Codes that were Cleaned: ", len(ziphyphencleaned)
    print "---------------------------------------------------------------------"

    '''Sample List of Cleansed ZipCodes'''
    
    print "Sample List of Cleansed ZipCodes"
    for i in range(len(ziphyphencleaned)): 
        if len(zipauto[i])>5 and count<=10: 
            print "Old Post Code: " + zipauto[i] + "--->" + "Cleaned Post Code: " + ziphyphencleaned[i]
            count = count + 1 
        else: 
            continue
    
    print "---------------------------------------------------------------------"
            
    '''List of Zipcodes to be Cleansed Manually'''
    print "List of Zipcodes to be Cleansed Manually"
    pprint.pprint(zipmanual)

    