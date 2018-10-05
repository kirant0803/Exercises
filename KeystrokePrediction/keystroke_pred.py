from nltk.tokenize import word_tokenize 
from nltk.tokenize import sent_tokenize
from nltk.util import ngrams
import operator

class Node:
    def __init__(self, label=None, data=None):
        self.label = label
        self.data = data
        self.children = dict()
    
    def addChild(self, key, data=None):
        if not isinstance(key, Node):
            self.children[key] = Node(key, data)
        else:
            self.children[key.label] = key
    
    def __getitem__(self, key):
        return self.children[key]

class Trie:
    def __init__(self):
        self.head = Node()
    
    def __getitem__(self, key):
        return self.head.children[key]
    
    def add(self, word):
        current_node = self.head
        word_finished = True
        
        for i in range(len(word)):
            if word[i] in current_node.children:
                current_node = current_node.children[word[i]]
            else:
                word_finished = False
                break
        
        # For ever new letter, create a new child node
        if not word_finished:
            while i < len(word):
                current_node.addChild(word[i])
                current_node = current_node.children[word[i]]
                i += 1
        
        # Let's store the full word at the end node so we don't need to
        # travel back up the tree to reconstruct the word
        current_node.data = word
    
    def has_word(self, word):
        if word == '':
            return False
        if word == None:
            raise ValueError('Trie.has_word requires a not-Null string')
        
        # Start at the top
        current_node = self.head
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break
        
        # Still need to check if we just reached a word like 't'
        # that isn't actually a full word in our dictionary
        if exists:
            if current_node.data == None:
                exists = False
        
        return exists
    
    def start_with_prefix(self, prefix):
        """ Returns a list of all words in tree that start with prefix """
        words = list()
        if prefix == None:
            raise ValueError('Requires not-Null prefix')
        
        # Determine end-of-prefix node
        top_node = self.head
        for letter in prefix:
            if letter in top_node.children:
                top_node = top_node.children[letter]
            else:
                # Prefix not in tree, go no further
                return words
        
        # Get words under prefix
        if top_node == self.head:
            queue = [node for key, node in top_node.children.iteritems()]
        else:
            queue = [top_node]
        
        # Perform a breadth first search under the prefix
        # A cool effect of using BFS as opposed to DFS is that BFS will return
        # a list of words ordered by increasing length
        while queue:
            current_node = queue.pop()
            if current_node.data != None:
                # Isn't it nice to not have to go back up the tree?
                words.append(current_node.data)
            
            queue = [node for key,node in current_node.children.iteritems()] + queue
        
        return words
    
    def getData(self, word):
        """ This returns the 'data' of the node identified by the given word """
        if not self.has_word(word):
            raise ValueError('{} not found in trie'.format(word))
        
        # Race to the bottom, get data
        current_node = self.head
        for letter in word:
            current_node = current_node[letter]
        
        return current_node.data

def next_word(text, word):
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
    if word in final_mapped.keys():
        return final_mapped[word]
    else:
        return "The word you typed isnt present in the data"


if __name__ == '__main__':
    """ Example use """
    trie = Trie()
    words = 'quick brown fox is lazy. queue is long'
    for word in words.split():
        trie.add(word)

    input_half_word = str(raw_input("Please type a word half :  "))
    top_words = trie.start_with_prefix(input_half_word)[:3]
    print list(set([x.lstrip(input_half_word)[0] for x in top_words]))

    input_word = str(raw_input("Please type a word full :  "))
    print next_word(words, input_word)