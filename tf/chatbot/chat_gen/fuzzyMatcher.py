from . import Matcher
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class FuzzyMatcher(Matcher):

    '''
    similarity computation
    '''

    def __init__(self, segLib = "jieba", removeStopWords = False):
	super().__init__(segLib)
	self.cleanStopWords = removeStopWords
	if removeStopWords:
	    self.loadStopWords("../knowledge_base/stopwords/chinese_sw.txt")
	    self.loadStopWords("../knowledge_base/stopwords/specialMarks.txt")

    def joinTitles(self):
	self.segTitles = ["".join(title) for title in self.segTitles]
	
    def tieBreak(self, query, i, j):
	'''
	choose one among articles having equal similarity
	
	Args:
	    - query: input query
	    - i: title having index of i
	    - j: title having index of j
	
	Return: (target, index)
	    - target: appropriate titles
	    - index: id of the title

	'''
	raw1 = self.titles[i]
	raw2 = self.titles[j]

	r1 = fuzz.ratio(query, raw1)
	r2 = fuzz.ratio(query, raw2)

	if r1 > r2:
	    return (raw1, i)
	else:
	    return (raw2, j)

	
    def match(self, query):
	'''
	read input query, return the sentence and tag if find one

	Args:
	    - query: sentences to be queried
	    - removeStopWords: remove stopwords
	'''

	if self.cleanStopWords:
	    mQuery = [word for word in self.wordSegmentation(query)
		      if word not in self.stopwords]
	    mQuery = "".join(mQuery)
	    title_list = self.segTitles
	else:
	    title_list = self.titles
	    mQuery = query

	for index, title in enumerate(title_list):
	    newRatio = fuzz.ratio(mQuery, title)

	   if newRatio > ratio:
		ratio = newRatio
		target = title
		target_idx =index

	    elif self.cleanStopWords and newRatio == ratio:
		target, target_idx = self.tieBreak(query, target_idx, index)

	self.similarity = ratio
	return target, target_idx
