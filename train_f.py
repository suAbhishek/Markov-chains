import re

class MarkovChain:
    def __init__(self):
        self.tree = dict()

    def train(self,txt, factor = 1):
        #extracting words from the text
        words = filter(lambda str: len(str)>0, re.split(r'[\s]',txt))

        #converting each letter of word in words lower case
        words = [w.lower() for w in words]

        for a,b in [(words[i],words[i+1]) for i in range(len(words)-1)]:
            if a not in  self.tree:
                self.tree[a] = dict()

            if b not in self.tree[a]:
                self.tree[a][b] = factor
            else:
                self.tree[a][b] = self.tree[a][b] + self.tree[a][b]*factor




