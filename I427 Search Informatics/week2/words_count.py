import sys
from collections import Counter
def words_count(file_name):
    with open (file_name,'r') as md_file:
        content = md_file.read().lower().split(' ')
    with open ('stopwords.txt','r') as sw_file:
        stopwords = [x.strip() for x in sw_file.readlines()]
    content = [x for x in content if x not in stopwords]
    #print(Counter(content).most_common(10))
    file_dict = dict(Counter(content).most_common(10))
    print(file_dict)
    # if __name__ == '__main__':
    # words_count(sys.argv[1])
def main(args):
    words_count(args[1])
if __name__ == '__main__':
    main(sys.argv)
