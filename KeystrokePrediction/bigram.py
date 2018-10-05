
from nltk.tokenize import word_tokenize 
from nltk.tokenize import sent_tokenize
from nltk.util import ngrams
import operator

text = """My name is Kiran. How are you doing? 
        I am working in a company thats started 100 years back.
        How are you guys? I am doing great.
        Are they doing fine?"""
sentences = sent_tokenize(text.lower())
bigrams = []
for line in sentences:
    token = word_tokenize(line.replace('.','').replace('?','').replace(',', ''))
    bigrams.extend(list(ngrams(token, 2)))
#print bigrams

BigD = {}
for bigram in bigrams:
    BigD[bigram[0]]={}

for i in BigD.keys():
    for bigram in bigrams:
        if i==bigram[0] and bigram[1] not in BigD[i].keys():
            BigD[i][bigram[1]] = 1
        elif i==bigram[0] and bigram[1] in BigD[i].keys():
            BigD[i][bigram[1]]+=1

final_mapped = {}
for a, b in BigD.iteritems():
    mapping_word = sorted(b.items(), key=operator.itemgetter(1))[-1][0]
    final_mapped[a] = mapping_word
print final_mapped


