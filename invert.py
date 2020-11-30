import re
import json
import os
from nltk.stem import PorterStemmer

class Invert:
    skipRegex = r'[\|\>\<\=\+\/\,\:\*\-\.\'\";\?\{\}\[\]\(\)\s]'
    ps = PorterStemmer()

    def __init__(self, documentsPath, stemming = True, stopWordRemoval = True):
        self.stemming = stemming
        self.stopWordRemoval = stopWordRemoval
        self.stopWords = self.getStopWords()
        self.index = {}
        self.documentsPath = os.path.join(os.path.dirname(__file__), documentsPath)

    def getStopWords(self):
        stopWords = set()
        with open('stopwords.txt', 'r') as stopWordsFile:
            for word in stopWordsFile:
                stopWords.add(word.rstrip().lower()) #make sure stop words are all lowercase
        return stopWords

    def buildIndex(self):
        with open(self.documentsPath, 'r') as documentsFile:
            documents = json.load(documentsFile)
            for doc in documents:
                self.__tokenizeAndUpdate(doc["url"][0], doc["body"][0])

    def __tokenizeAndUpdate(self, url, text):
        terms = re.split(self.skipRegex + '+', text)
        alreadyUpdated = set()
        
        for term in terms:
            if self.stemming:
                lowercaseTerm = self.ps.stem(term.lower())
            else:
                lowercaseTerm = term.lower()

            skipTerm = (self.stopWordRemoval and lowercaseTerm in self.stopWords) or (len(term) == 1 and re.match('[^ai]', lowercaseTerm))

            if len(term) > 0 and not skipTerm:
                if not lowercaseTerm in self.index:
                    self.index[lowercaseTerm] = [1, [[url, 1]]]
                    alreadyUpdated.add(lowercaseTerm)
                elif not lowercaseTerm in alreadyUpdated:
                    self.index[lowercaseTerm][0] += 1   # increase doc frequency
                    self.index[lowercaseTerm][1].append([url, 1])   #in index but first occurrence in doc
                    alreadyUpdated.add(lowercaseTerm)
                else:
                    self.index[lowercaseTerm][1][-1][1] += 1    #in index and nth occurence in doc, increment tf by 1

invert = Invert('crawler/pages.json')
invert.buildIndex()
print("done")