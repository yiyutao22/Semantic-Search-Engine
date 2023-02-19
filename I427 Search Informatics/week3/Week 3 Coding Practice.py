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
    for key, value in file_dict.items():
    	#round to three significant figures
        file_dict[key] = round(value/len(content),4)
    return file_dict


def words_count_f(folder_path):
    dirs = os.listdir(folder_path)
    file_dict = {}
    for file in dirs:
        #filter out trash file 
        if 'txt' in file:
            file_dict[file] = words_count(file)
    print(file_dict)

words_count_f('/Users/mac/Documents/I427/week3/')
