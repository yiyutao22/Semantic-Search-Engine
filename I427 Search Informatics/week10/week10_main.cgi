#! /usr/bin/env python3
print('Content-type: text/html\n')

import cgi
form = cgi.FieldStorage()  

html = """<!doctype html>
<html>
	<head><meta charset="utf-8">
	<link rel="stylesheet" href="https://cgi.sice.indiana.edu/~dpierz/i211.css">
	<title>Week 10</title>
	</head>
	<body>
		{content}
	</body>
</html>"""


terms = form.getfirst('term','')

import sys, os
import re
import nltk
from nltk.stem import PorterStemmer 
from collections import Counter
from nltk.corpus import stopwords
import math

ps = PorterStemmer() 
def words_count(file_name):
    with open (file_name,'r') as md_file:
        content = md_file.read()
    #remove punctuation
    content = re.sub('[^A-Za-z0-9]+', ' ', content)
    count = len(content)
    content = nltk.word_tokenize(content.lower())
    #remove stopwords
    content = [word for word in content if not word in stopwords.words()]
    for i in range(len(content)):
        #stemming words
        content[i] = ps.stem(content[i])
    file_dict = dict(Counter(content))
    for key, value in file_dict.items():
        #norm tfs
        file_dict[key] = value/count
    return file_dict
    
def words_count_f(folder_path):
    dirs = os.listdir(folder_path)
    file_dict = {}
    for file in dirs:
        #filter out trash file 
        if 'html' in file and 'week10' not in file:
            file_dict[file] = words_count(file)
    return file_dict

value_dict = words_count_f('/u/yiyutao/cgi-pub/I427/week10')

#define a new function return mapping_dict, contains index number and txt file names
def return_file(folder_path):
    dirs = os.listdir(folder_path)
    mapping_dict = dict(enumerate(dirs))
    return mapping_dict

mapping_dict = {}

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
    for k, subdict in value_dict.items():
        for key, value in mapping_dict.items():
            #check which txt file it is
            if k == value:
                #loop through each term and its frequency
                for kk, v in subdict.items():
                    inv_index.setdefault(kk, {})[key] = v
    return inv_index, mapping_dict

mapping_dict = inv_indexer(mapping_dict, value_dict, inv_index)[1]

tf_idf = {}
def tf_idf_q(folder_path, terms):
    value_dict = words_count_f(folder_path)
    all_terms = []
    for each_file in value_dict.values():
        full_lst = list(each_file.keys())
        for each in full_lst:
            all_terms.append(each)
    #calculate idf for each unique term
    idf = dict(Counter(all_terms))
    for key, value in idf.items():
        idf[key] = 1/(1+math.log10(value))
    mapping_dict = {}
    for key in value_dict.keys():
        if key not in mapping_dict.values():
            if not mapping_dict.keys():
                mapping_dict[1] = key
            else:
                mapping_dict[int(max(mapping_dict.keys())+1)] = key
    for key in list(mapping_dict.values()):
        tf_idf[key] = sum([idf[each]*value_dict[key][each] for each in list(idf.keys())
                           if each in list(value_dict[key].keys())])
    user_input = list(terms.strip().split())
    #corresponding tf-idf score
    for file, subdict in value_dict.items():
        for content in subdict.values():
            for word in user_input:
            	if word in content:
                    sub_dict = {}
                    sub_dict[file] = tf_idf[file]
                    for each in sub_dict.items():
                        print(each)
    
content = tf_idf_q('/u/yiyutao/cgi-pub/I427/week10', terms)
    
print(html.format(content = content))

    
    
    
    