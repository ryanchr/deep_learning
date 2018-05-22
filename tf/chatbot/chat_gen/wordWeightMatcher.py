import math
import logging
import gensim

from collections import defaultdict
from . import Matcher

class WordWeightMatcher(Matcher):
    '''
    use word weight for computing phrase similarity
    '''

    def __init__(self, segLib="jieba"):

        super().__init__(segLib)

        self.wordDict = defaultdict(int) #record word freq
        self.totalWords = 0 # word count
        self.wordWeights = defaultdict(int) #record word weight


    def initialize(self):
        logging.info("initializing module")
        self.TitlesSegmentation()
        self.buildWordDict()
        self.loadStopWords('../knowledge_base/stopwords/chinese_sw.txt')
        self.loadStopWords('../knowledge_base/stopwords/specialMarks.txt')
        self.calculateWeight()
        logging.info("Completed initialization")

    def buildWordDict(self):

        for title in self.segTitles:
            for word in title:
                self.wordDict[word] += 1
                self.totalWords += 1

        logging.info("Completed word count")

    def buildWordBag(self):
        dict = gensim.corpora.Dictionary(self.titles)


    def computeWeigh(self):
        '''
        IDF weight calculation:
            http://www.52nlp.cn/forgetnlp4
            weight here used is -1 * log(N/T)
        '''

        for word, count in self.wordDict.items():
            self.wordWeights[word] = -1 * math.log10(count/self.totalWords)
        logging.info("Completed word statistics")


    def getCoConcurrence(self, q1, q2):
        res = []
        for word in q1:
            if word in q2:
                res.append(word)
        return res


    def getWordWeight(self, word, n=1):
        return (n * self.wordWeights[word])


    def match(self, query, sort=False):
        '''
        read input query, return matched sentence and title
        '''


        max_similarity = -1
        target = ""
        index = -1

        segQuery = [word for word in self.wordSegmentation(query)
                    if word not in self.stopwords]

        for index, title in enumerate(self.segTitles):
            if len(title) == 0:
                continue

            allWordsWeight = 0.
            coWordsWeight = 0.

            coWords = self.getCoConcurrence(title, segQuery)

            for word in coWords:
                coWordsWeight += self.getWordWeight(word)

            for word in title:
                if word not in coWords:
                    allWordsWeight += self.getWordWeight(word)
            for word in seqQuery:
                if word not in coWords:
                    allWordsWeight += self.getWordWeight(word)

            similarity = coWordsWeight / allWordsWeight

            if similarity > max_similarity:
                max_similarity = similarity
                target = title
                target_idx = index


        self.similarity = max_similarity * 100

        return target, target_idx

