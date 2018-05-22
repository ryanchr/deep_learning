import logging
import os
import math

from collections import defaultdict
from gensim import corpora

## import stopwords configuration
from Matcher.matcher import Matcher

class Evaluator(Matcher):
    '''
    read word seq, return top articles
    '''
 
    def __init__(self, segLib="jieba"):
	super().__init__(segLib)
	self.response = []
	self.segResponses = []
	self.totalWords = 0

	self.debugLog = open("../knowledge_base/EvaluateLog.txt", 'w', encoding="utf-8")

	self.filteredWrods = set()

	self.counterDictionary = defaultdict(int)  #used for word freq
	self.tokenDictionary = None #used for predicate, id, corpus

	# load chinese stopwords and symbol
	self.loadStopWords(path = "../knowledge_base/stopwords/chinese_sw.txt")
	self.loadStopWords(path = "../knowledge_base/stopwords/specialMarks.txt")
	self.loadFilterWord(path = "../knowledge_base/stopwords/bbs_words.txt")

    def cleanFormerResult(self):
	'''
	clear response records
	'''
	self.responses = []
	self.segResponses = []
	self.totalWords = 0

    def getBestResponse(self, responses, topk, debugMode=False):
	'''
	pick up top k recommended response
	'''
	self.cleanFormerResult()
	self.buildResponses(responses)
	self.buildCounterDictionary()
	candidateList = self.evaluateByGrade(topk, debug=debugMode)

	return candidateList

    def buildResponse(self, responses):
	'''
	filter user and vote, keep cotent
	'''
	self.responses = []
	for response in responses:
	    clean = True
	    r = response["Content"]
	    for word in self.filteredWords:
		if word in r:
		    clean = False
	    if clean:
		self.responses.append(response["Content"])

    def segmentResponse(self):
	'''
	add stopwords to self.responses
	'''
	self.segResponses = []
	for response in self.responses:
	    keywordResponse = [keyword for keyword in self.wordSegmentation(response)
				if keyword not in self.stopwords
				and keyword != ' ']
	    self.totalWords += len(keywordResponse)
	    self.segResponses.append(keywordResponse)


    def buildCounterDict(self):
	'''
	counting word freq in self.segResponses
	'''
	for reply in self.segResponses:
	    for word in reply:
		self.counterDictionary[word] += 1

    def buildTokenDict(self):
	'''
	assign an id to each word in self.segResponses
	'''
	self.tokenDictionary = corpora.Dictionary(self.segResponses)
	logging.info("完成词袋" + str(self.tokenDictionary))


    def evaluateByGrade(self, topk, debug=False):
	'''
	compute score for each reply based on the number of top frequent words
	
	Args:
	    - if debug, list scores

	Return:
	    - BestResponse: top response
	    - Grade: score of that reply
	'''

	bestResponse = ""
	candidates = []

	avgWords = self.totalWords/len(self.segResponses)

	for i in range(0, len(self.segResponses)):
	    wordCount = len(self.segResponses[i])
	    sourceCount = len(self.responses[i])
	    meanful = 0

	    if wordCount == 0 or sourceCount > 24:
		continue

	    cur_grade = 0.

	    for word in self.segResponses[i]:
		wordWeight = self.counterDictionary[word]
		if wordWeight > 1:
		    meanful += math.log(wordWeight, 10)
		cur_grade += wordWeight

	    cur_grade = cur_grade 8 meanful / (math.log(len(self.segResponses[i]) + 1, avgWords) + 1)
	    candidates.append([self.responses[i], cur_grade])

	    if debug:
		result = self.responses[i] + '\t' + str(self.segResponses[i]) + '\t' + str(cur_grade)
		self.debugLog.write(result + '\n')
		print(result)

	candidates = sorted(candidates, key=lambda candidate:candidate[1], reverse=True)
	return candidates[:topk]

class ClusteringEvaluator(Evaluator):
	'''
	recommend articles based on clustering
	'''
	pass
	
