# Importing all the Needed Libraries
import re
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict


'''Regular Expressions for different kinds of Cleaning'''
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

filename = 'Boston.osm'



'''Function that does the phone number cleanse through an iterative process'''
def clean_phone(): 
    
    '''For loop to check for alphabets in the phonenumber. Phone Numbers that have alphabets
    are populated in a seperate list for manual review. Phone numbers that do not have any alphabets proceed along
    to other steps in the cleaning process '''
    for phone_item in read_key:
        match=phonecheckalpha.search(phone_item)
        if match: 
            phone_list1Manual.append("To be Review Manually:" + phone_item)
        else:
            phone_list1.append(phone_item)

    '''For Loop to cleanse any whitespaces in the phonenumber'''
    for phonelist1_item in phone_list1: 
        match=phonecheckspace.search(phonelist1_item)
        if match: 
            phonelist1_itemnew=phonelist1_item.replace(match.group(0), '')
            phone_list2.append(phonelist1_itemnew)
        else: 
            phone_list2.append(phonelist1_item)
    
    '''For Loop to cleanse any Hyphens in the phonenumber'''
    for phonelist2_item in phone_list2: 
        match = phonecheckhyphen.search(phonelist2_item)
        if match: 
            phonelist2_itemnew = phonelist2_item.replace(match.group(0), '')
            phone_list3.append(phonelist2_itemnew)
        else: 
            phone_list3.append(phonelist2_item)
    
    '''For Loop to cleanse any phonenumbers that start with +1 '''  
    for phonelist3_item in phone_list3: 
        match = phonecheckone.search(phonelist3_item)
        if match: 
            phonelist3_itemnew = phonelist3_item.replace(match.group(0), '')
            phone_list4.append(phonelist3_itemnew)
        else: 
            phone_list4.append(phonelist3_item)
    
    '''For loop to cleanse any paranthesis in the phonenumber'''
    for phonelist4_item in phone_list4: 
        match = phonecheckpar1.search(phonelist4_item)
        if match: 
            phonelist4_itemnew = phonelist4_item.replace(match.group(0), '')
            phone_list5.append(phonelist4_itemnew)
        else: 
            phone_list5.append(phonelist4_item)

    
    for phonelist5_item in phone_list5: 
        match = phonecheckpar2.search(phonelist5_item)
        if match: 
            phonelist5_itemnew = phonelist5_item.replace(match.group(0), '')
            phone_list6.append(phonelist5_itemnew)
        else: 
            phone_list6.append(phonelist5_item)
    
    '''For loop to cleanse any periods in the phonenumber'''
    for phonelist6_item in phone_list6: 
        match = phonecheckperiod.search(phonelist6_item)
        if match: 
            phonelist6_itemnew = phonelist6_item.replace(match.group(0), '')
            phone_list7.append(phonelist6_itemnew)
        else: 
            phone_list7.append(phonelist6_item)

    '''For loop to cleanse any phone numbers that begin with a 1'''
    for phonelist7_item in phone_list7: 
        if phonelist7_item.startswith('1') or phonelist7_item.startswith('+') : 
            phone_list8.append(phonelist7_item[1:])
        else: 
            phone_list8.append(phonelist7_item)

    '''For loop to cleanse any commas in the phonenumbers'''
    for phonelist8_item in phone_list8: 
        match = phonecheckcomma.search(phonelist8_item)
        if match: 
            phonelist8_itemnew = phonelist8_item.replace(match.group(0), '')
            phone_list9.append(phonelist8_itemnew)
        else: 
            phone_list9.append(phonelist8_item)
        
def checkalphabetsfromsource(): 
     for phonevalue in read_key:
        match=phonecheckalpha.search(phonevalue)
        if match: 
            phone = phonevalue.replace(match.group(0), '')
            phoneset_alpha.append(phonevalue)
        else: 
            phoneset_noalpha.append(phonevalue)

    
       
def read_file():
    for _, element in ET.iterparse(filename): 
        for child in element.getchildren(): 
            if child.tag=='tag': 
                key=child.get('k')
                if 'phone' in key: 
                    phone_number = child.get('v')
                    phone_set.append(phone_number)
    return phone_set
                

if __name__ == "__main__":
    count = 0 
    
    '''Initializing the different list before using them through the 
    different steps of the cleanse process with the regular expression'''
    
    
    phone_set = []
    phoneset_alpha=[]
    phoneset_noalpha=[]
    phone_list1=[]
    phone_list1Manual=[]
    phone_list2=[]
    phone_list3=[]
    phone_list4=[]
    phone_list5=[]
    phone_list6=[]
    phone_list7=[]
    phone_list8=[]
    phone_list9=[]
    
    
    
    read_key = read_file()
    clean_phone = clean_phone()
    check_alphabets = checkalphabetsfromsource()
    
    
    
    
    print "Phone Number Cleansing High Level Stats"
    print "-------------------------------------------------"
    print "Total Number of Phone Numbers to be Validated", len(read_key)
    print "Total Number Cleaned Up Phone Numbers: ", count 
    print "Total Number of Phone Numbers to be cleaned Manually: ", len(phone_list1Manual) 
    print "List of Phone Numbers to be Cleaned Manually" 
    pprint.pprint(phone_list1Manual)
    print "-------------------------------------------------"
    
    
    '''Sample List of Cleansed Phone Numbers'''
    print "Sample List of Cleansed Phone Numbers"
    for i in range(len(phone_list1)): 
        if len(phone_list9[i])==10 and count<=10: 
            print phone_list1[i],    "--->" ,  phone_list9[i]
            count = count + 1 
            
        elif len(phone_list9[i])>10: 
            phone_list1Manual.append("To be Review Manually:" + phone_list9[i])
        
        else: 
            continue
    '''List of PhoneNumbers to be Cleansed Manually'''
    print "List of PhoneNumbers to be Cleansed Manually"
    pprint.pprint(phone_list1Manual)
    