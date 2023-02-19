import sys, os
import re
import nltk
import json
from nltk import flatten
from nltk.stem import PorterStemmer 
from collections import Counter
from nltk.corpus import stopwords

ps = PorterStemmer() 
def words_count(file_name):
    with open (file_name,'r') as md_file:
        content = md_file.read()
    content = nltk.word_tokenize(content.lower())
    #remove stopwords
    content = [word for word in content if not word in stopwords.words()]
    """
    content = re.sub('[^A-Za-z0-9]+', ' ', content)
    content = content.splitlines()
    for i in range(len(content)):
        content[i] = content[i].lower().split(' ') 
    content = flatten(content)
    """
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
value_dict = words_count_f('/Users/mac/Documents/I427/week5/')

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
                mapping_dict[1] = key
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
    return inv_index, mapping_dict
    
""" 
    Due to unknown reason, the order of reading files is messed up
    Please check the print statement of mapping_dict
"""    
mapping_dict = inv_indexer(mapping_dict, value_dict, inv_index)[1]
print(mapping_dict)

inv_index_dict = inv_indexer(mapping_dict, value_dict, inv_index)[0]
#print(inv_index_dict)

"""
output each subdict to multiple json files, name the file with each text file name
for key, value in value_dict.items():
    with open("{}.json".format(key), "w") as outfile:  
        json.dump(value, outfile) 
"""

lst = []
sub_dict = {}
ranking_dict = {}

def search_words(inv_index_dict):
    #get user input as a list
    user_input = list(input("Please enter the term(s) you want to search: ").strip().split())
    #check if all input terms exist in the dict
    if all(word in inv_index_dict.keys() for word in user_input):
        for word in user_input:
            #append the list of documents for each term to a large nested list
            lst.append([int(k) for k in inv_index_dict[word].keys()])
            #create a sub dict only contains terms we search
            sub_dict[word] = inv_index_dict[word]
        print(sub_dict)
        #find the intersection
        result = set.intersection(*[set(x) for x in lst]) 
        if result:
            for each in result:
                #use sub dict to sum the ranking values of each common key
                ranking_values = sum(d[each] for d in sub_dict.values())
                ranking_dict[mapping_dict[each]] = ranking_values
            #sort the dict by the ranking values in descending order
            for k in sorted(ranking_dict, key=ranking_dict.get, reverse=True):
                print(k, ranking_dict[k])
        else:
            print("Common documents don't exist.")
    else: 
        print("Invalid input! Please try again.")
    
search_words(inv_index_dict)
