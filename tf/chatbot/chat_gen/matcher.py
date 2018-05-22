import logging
import os
import jieba

try:
    import Taiba
except:
    pass

class Matcher(object):
    '''
    compare query and corpus, return a sentence
    '''

    def __init__(self, segLib="jieba"):
	logging.basicconfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
	self.titles = [] # titles to be matched
	self.segTitles = [] # titles inserted stopper

	self.stopwords = set()
	self.similarity = 1.

	if segLib == "jieba":
	    self.useJieba = True
	    logging.info("[Mather]: Select jieba for word segment.")

    def jiebaCustomSetting(self, dict_path, usr_dict_path):
	jieba.set_dictionary(dict_path)
	with open(usr_dict_path, 'r', encoding='utf-8') as dic:
	    for word in dic:
		jieba.add_word(word.strip('\n'))

    def loadStopWords(self, path):
	with open(path, 'r', encoding='utf-8') as sw:
	    for word in sw:
		self.stopwords.add(word.strip('\n')

    def loadTitles(self, path):
	with open(path, 'r', encoding='utf-8') as data:
	    self.titles = [line.strip('\n') for line in data]

    def match(self, query):
	'''
	read input query, and return matched title and sentence
	
	Args:
	    - query: input 
	Return:
	    - title: similar title
	    - index tag for the title
	'''

	result = None
	for index, title in enumerate(self.titles):
	    if title == query:
		return title, index

    def getSimilarity(self):
	return self.similarity

    def wordSegmentation(self, string):
	tp = None

	if self.useJieba:
	    tp = jieba.cut(string, cut_all=True)

	return [q for q in tp]


def TitlesSegmentation(self, cleanStopwords=False):
    logging.info("Start title segmentation")

    count = 0
    if not os.path.exists('../knowledge_base/SegTitles.txt')
        self.SegTitles = []
        for title in self.titles:

            if cleanStopWords:
                clean = [word for word in self.wordSegmentation(title)
                         if word not in self.stopWords ]
                self.SegTitles.append(clean)
            else:
                self.SegTitless.append(self.wordSegmentation(title))

            count += 1
            if count % 1000 == 0:
                looging.info("Completed segmentation for % d articles" % count)

        with open('../knowledge_base/SegTitles.txt'., 'w', encoding='utf-8') as dataSegTitle:
            for title in self.segTitles:
                dataSegTitle.write(' '.join(title) + '\n')
        logging.info("Completed word segment, saved data to knowledge_base/SegTitles.txt")
    else:
        logging.info("read prior segmentation result")
        with open('../knowledge_base/SegTitles.txt', 'r', encoding='utf-8') as dataSegTitle:
            for line in dataSegTitle:
                line = line.strip('\n')
                seg = line.split()

                if cleanStopWords:
                    seg = [word for word in seg
                            if word not in self.stopWords]
                self.segTitles.append(seg)
            looging.info("%d titles have been loaded" % len(self.segTitles))





