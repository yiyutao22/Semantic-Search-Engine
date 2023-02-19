#! /usr/bin/env python3
print('Content-type: text/html\n')

import cgi, json

form = cgi.FieldStorage()

html = """<!doctype html><html>    
<head>  
<meta charset="utf-8">   
<link rel="stylesheet" href="https://cgi.sice.indiana.edu/~dpierz/i211.css">
<title>Results</title>    
</head>    
<body>   
<p>{content}</p>    
</body></html>"""

term = form.getvalue('term','').strip().split()

with open('tfidf.json','r') as file: tf_idf = json.load(file)
with open('file.json','r') as file: file = json.load(file)

lst = []
sub_dict = {}

for word in term: 
	for key, value in file.items(): 
		if word in value: 
			lst.append(key)
result = set([x for x in lst if lst.count(x) > 1])
if result:
	for file in result:
		sub_dict[file] = tf_idf[file]

	sorted_dict = {}
	sorted_keys = sorted(sub_dict, key=sub_dict.get, reverse=True)
	for w in sorted_keys:
    		sorted_dict[w] = sub_dict[w]	
	print(html.format(content = sorted_dict))
else:
	print(html.format(content = 'Please try again!'))

