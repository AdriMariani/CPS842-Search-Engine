from invert import Invert
import re
import math
import json
import os
import networkx
from nltk.stem import PorterStemmer

class Search:
    regex = skipRegex = r'[\|\>\<\=\+\/\,\:\*\-\.\'\";\?\{\}\[\]\(\)\s]'
    ps = PorterStemmer()
    cosineWeight = 0.75
    pageRankWeight = 0.25

    def __init__(self, documentsPath, stemming = True, stopWordRemoval = True):
        invert = Invert(documentsPath, stemming, stopWordRemoval)
        invert.buildIndex()
        self.index = invert.index
        self.stemming = stemming
        self.stopWordRemoval = stopWordRemoval
        self.documentsPath = os.path.join(os.path.dirname(__file__), documentsPath)
        self.docCollection = self.__getCollection()
        self.pageRank = self.__calculatePageRank()
        self.stopWords = invert.stopWords

    def __getCollection(self):
        collection = {}
        with open(self.documentsPath, 'r') as documentsFile:
            documents = json.load(documentsFile)
            for doc in documents:
                collection[doc["url"][0]] = { "title": doc["title"][0], "outLinks": doc["outLinks"] }
        return collection

    def __calculatePageRank(self):
        graph = networkx.DiGraph()
        for doc in self.docCollection:
            for link in self.docCollection[doc]["outLinks"]:
                graph.add_edge(doc, link)
        return networkx.pagerank(graph)   # default alpha is 0.85

    def query(self, queryText):
        terms = [term.lower() for term in re.split(self.skipRegex + '+', queryText)]
        docVectors = {}
        queryFrequencies = {}
        idfValues = {}
        numberOfTerms = 0
    
        for term in sorted(terms):
            if self.stemming:
                term = self.ps.stem(term)

            skipTerm = (not term in self.index) or (self.stopWordRemoval and term in self.stopWords)

            if not skipTerm and term in queryFrequencies:
                queryFrequencies[term] += 1
            elif not skipTerm:
                idf = math.log10(len(self.docCollection) / self.index[term][0])
                idfValues[term] = idf
                
                for doc in self.index[term][1]:
                    weight = (1 + math.log10(doc[1])) * idf
                    if not doc[0] in docVectors:    # if this document has not been seen yet, must add 0's for all terms not in document
                        vector = []
                        for i in range(0, numberOfTerms):
                            vector.append(0)
                        vector.append(weight)
                        docVectors[doc[0]] = vector
                    else:
                        docVectors[doc[0]].append(weight)

                numberOfTerms += 1
                queryFrequencies[term] = 1
                
                for doc in docVectors:  # for any terms that didn't have the term, add a 0 as the weight
                    if len(docVectors[doc]) < numberOfTerms:
                        docVectors[doc].append(0)

        queryVector = []
        for term in sorted(queryFrequencies.keys()):
            tf = 1 + math.log10(queryFrequencies[term])
            queryVector.append(tf * idfValues[term])

        return self.__calculateRankings(queryVector, docVectors)

    def __calculateRankings(self, queryVector, docVectors):
        scores = {}
        queryVectorLength = math.sqrt(sum([w*w for w in queryVector]))

        for doc in docVectors:
            docVectorLength = math.sqrt(sum([w*w for w in docVectors[doc]]))
            scalarProduct = 0
            for i in range(0, len(queryVector)):
                scalarProduct += docVectors[doc][i] * queryVector[i]
            cosineSimilarity = scalarProduct / (queryVectorLength * docVectorLength)
            scores[doc] = self.cosineWeight * cosineSimilarity + self.pageRankWeight * self.pageRank[doc]

        # sort by cosine similarity
        return [{"url": k, "score": v, "title": self.docCollection[k]["title"]} for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)]