import os
import pandas
import nltk
from nltk.stem import WordNetLemmatizer 
nltk.download('wordnet')

#Get corpus directory
root = os.getcwd()
corpus_dir = '/corpus/'
special_character_dir = '/specialchar.txt'
with open(root+special_character_dir) as specialchar_doc:
    special_character_list = specialchar_doc.read().split()
corpus_list = os.listdir(root+corpus_dir)
corpus_list.sort()
posting_list = {}
#Helper function
def print_posting(a):
    print('{:<12}{:<12}{:<12}'.format('Word', 'Frequency','Posting'))
    for i in a:
        print('{:<12}{:<12}{:<12}'.format(i, str(a[i][0]), ' -> '.join(a[i][1])))
#Create inverted index posting list
lemmatizer = WordNetLemmatizer()
for f in corpus_list:
    with open(root+corpus_dir+f, 'r') as corpus_file:   
        doc = corpus_file.read()
        for sc in special_character_list:
            doc = doc.replace(sc, '')
        doc = doc.split()
    for i in doc:
        index = i.lower()
        index = lemmatizer.lemmatize(index)
        if index not in posting_list:
            posting_list[index] = [0,[]]
        posting_list[index][0] += 1 
        if f not in posting_list[index][1]:
            posting_list[index][1].append(f)
#Constructing bitmap from query
query_string = input("Enter query string:\n")
query_string = query_string.lower()
connect_word = []
query_word = []
for i in query_string.split():
    if i != 'and' and i != 'or' and i != 'not':
        query_word.append(i)
    else:
        connect_word.append(lemmatizer.lematize(i))
bitmap = pandas.DataFrame(columns=corpus_list, index=query_word)
for word in query_word:
    for doc in corpus_list:
        if word not in posting_list:
            bitmap[doc][word] = 0
        elif doc in posting_list[word][1]:
            bitmap[doc][word] = 1
        else:
            bitmap[doc][word] = 0
#Query bitmap
all_query = []
single_query = []
i = 0
bit = 1
while i < len(query_word):
    single_query.append((query_word[i], bit))
    if i >= len(connect_word):
        break
    if connect_word[i] == 'not':
        bit = 0
    elif connect_word[i] == 'and':
        bit = 1
    else:
        all_query.append(single_query.copy())
        single_query.clear()
    i += 1
all_query.append(single_query.copy())
#print(all_query)
#Query
result = set()
for q in all_query:
    for doc in corpus_list:
        #print(doc)
        test = True
        for w in q:
            #print('w[0]: ', bitmap[doc][w[0]], w[1])
            if bitmap[doc][w[0]] != w[1]:
                test = False
        if test:
            result.add(doc)
print_posting(posting_list)
for r in result:
    print(r, end=' ')
print('\n')
                
