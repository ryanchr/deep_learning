import math

from . import Matcher
from . import QuickSearcher

class BestMatcher(Matcher):
    '''
    a phrase  matcher based on bm25 algorithm
    '''

    def __init__(self, segLib="jieba", removeStopWords=False):
	super().__init__(segLib)

	self.cleanStopWords = removeStopWords
	self.D = 0  # number of sentences

	self.wordset = set()  # a set of words in the corpus
	self.words_location_record = dict() # record word (key) to which sentence (id)
	self.words_idf = dict() # record idf value of each word

	self.f = []
	self. df = {}
	self.idf = {}
	self.k1 = 1.5
	self.b = 0.75

	self.searcher = QuickSearcher() #search for sentence

	if removeStopWords:
	    self.loadStopWords("../knowledge_base/stopwords/chinese_sw.txt")
	    self.loadStopWords("../knowledge_base/stopwords/speicalMarks.txt")

    
    def initilize(self, ngram=1):
	assert(len(self.titles) > 0, "请先载入短语表")
	
	self.TitlesSegmentation()  #divide self.titles
	self.initBM25()
	self.searcher.buildInvertedIndex(self.segTitles)

	'''
	'''

   def initBM25():
	print("Initializing BM25 module")

	self.D = len(self.segTitles)
	self.avgdl = sum([len(title) + 0.0 for title in self.segTitles]) / self.D

	for seg_title in self.segTitles:
	    tmp = {}
	    for word in seg_title:
		if not word in tmp:
		    tmp[word] = 0
		tmp[word] += 1
	    self.f.append(tmp)
	    for k, v in tmp.items():
		if k not in self.df:
		    self.df[k] = 0
		self.df[k] += 1
	for k,v in self.df.items():
	    self.idf[k] = math.log(self.D-v+0.5) - math.log(v+0.5)

	print("Completed initilization of BM25")


    def sim(self, doc, indx):
	score = 0
	for word in doc:
	    if word not in self.f[index]:
		continue
	    d = len(self.segTitles[index])
	    score += (self.idf[word] * self.f[index][word] * (self.k1+1)
		      /  (self.f[index][word] + self.k1*(1-self.b+self.b*d / self.avgdl)))

	return score

    def calculateIDF(self):
	#build word set and record word index
	if len(self.wordset) == 0:
	    self.buildWordSet()
	if len(self.words_location_record) == 0:
	    self.buildWordLocationRecord()

	for word in self.wordset:
	    self.words_id[word] = math.log2((self.D + .5) / (self.words_location_record[word] + .5))


    def buildWordLocationRecord(self):
	'''
	build dict containing word and word idx
	'''
	for idx, seg_title in enumerate(self.segTitles):
	    for word in seg_title:
		if self.words_location_record[word] is None:
		    self.words_location_record[word] = set()
		self.words_location_record[word].add(idx)

    def buildWordSet(self):
	'''
	build corpus set
	'''
	for seg_title in self.segTitles:
	    for word in seg_title:
		self.wordset.add(word)

    def addNgram(self, n):
	'''
	expand self.seg_titles to be n-gram
	'''
	idx = 0
	
	for seg_list in self.segTitles:
	    ngram = self.generateNgram(n, self.titles[idx]
	    seg_list = seg_list + ngram
	    idx += 1


    def generateNGram(self, n, sentence):
	return [sentence[i:i+n] for i in range(0,len(sentence)-1)]


    def joinTitles(self):
	self.segTitles = ["".join(title) for title in self.segTitles]


    def match(self, query):
	'''
	import query, return sentence and tag if found similar sentence in corpus
	Args:
	    - query: input sentence
	'''

	seg_query = self.wordSegmentation(query)
	max = -1
	target = ''
	target_idx = -1

	target_index = self.searcher.quickSearch(seg_query) # pick up titles

	for index in target_index:
	    score = self.sim(seg_query, index)
	    if score > max:
		target_idx = index
		max = score

	# normalization
	max = max / self.sim(self.segTitles[target_idx], target_idx)
	target = ''.join(self.segTitles[target_idx])
	self.similarity = max * 100 #

	return target, target_idx
