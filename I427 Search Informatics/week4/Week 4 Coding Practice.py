import sys, os
import re
from nltk import flatten
from nltk.stem import PorterStemmer 
from collections import Counter

ps = PorterStemmer() 
def words_count(file_name):
    with open (file_name,'r') as md_file:
        content = md_file.read()
        #remove punctuation 
        content = re.sub('[^A-Za-z0-9]+', ' ', content)
        #strip 
        content = content.splitlines()
    for i in range(len(content)):
        content[i] = content[i].lower().split(' ')
        #the list becomes a nested list 
    #convert to a single list 
    content = flatten(content)
    for i in range(len(content)):
        #stemming words
        content[i] = ps.stem(content[i])
    file_dict = dict(Counter(content))
    return file_dict


def words_count_f(folder_path):
    dirs = os.listdir(folder_path)
    file_dict = {}
    for file in dirs:
        #filter out trash file 
        if 'txt' in file:
            file_dict[file] = words_count(file)
    return file_dict

#contains output(nested dictionary) of last function
value_dict = words_count_f('/Users/mac/Documents/I427/week4/')
#value_dict = words_count_f('https://cgi.sice.indiana.edu/~yiyutao/I427/week4/')

#define a new function return mapping_dict, contains index number and txt file names
def return_file(folder_path):
    dirs = os.listdir(folder_path)
    mapping_dict = dict(enumerate(dirs))
    return mapping_dict

mapping_dict = {}
#mapping_dict = return_file('/Users/mac/Documents/I427/week4/')
#for key in mapping_dict.copy():
    #if 'txt' not in mapping_dict[key]:
        #del mapping_dict[key]

#create an empty dict as argument 
inv_index = {}

def inv_indexer(mapping_dict, value_dict, inv_index):
    for key in value_dict.keys():
        if key not in mapping_dict.values():
            if not mapping_dict.keys():
                #the first entry, start with 0
                mapping_dict[0] = key
            else:
                #plus one at a time
                mapping_dict[int(max(mapping_dict.keys())+1)] = key
    #count the total amounts of each term
    #inv_index = dict(sum(map(Counter, value_dict.values()),Counter())) 
    for k, subdict in value_dict.items():
        for key, value in mapping_dict.items():
            #check which txt file it is
            if k == value:
                #loop through each term and its frequency
                for kk, v in subdict.items():
                    """
                    use setdefault to return all values of same term in three subdict 
                    {} means zipping three or few values of each term into a new subdict
                    [key] is the index number in mapping_dict
                    v is the value
                    """
                    inv_index.setdefault(kk, {})[key] = v
    print(inv_index)
    """ 
    Due to unknown reason, the order of reading files is messed up, it's file2, file3, then file1.
    Please check the print statement of mapping_dict
    index 0 is file2.txt; index 1 is file3.txt; index 2 is file1.txt
    """
    print(mapping_dict)
    

inv_indexer(mapping_dict, value_dict, inv_index)

