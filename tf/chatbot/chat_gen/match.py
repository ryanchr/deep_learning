import json
import os 
import random

from responsesEvaluate import Evaluator
from Matcher.fuzzyMather import FuzzyMather
from Matcher.wordWeightMatcher import WordWeightMatcher
from Matcher.bm25Matcher import bestMatchingMatcher

from Matcher.matcher import Matcher

def main():
    matcherTesting("bm25", removeStopWords=False)


def getMatcher(matcherType, removeStopWords=False):
    '''
    return initilized matcher

    Args:
	- matcherType: types of matching word seq
	    - Fuzzy
	    - WordWeigth
	- sort:
	    - a boolean value for fuzzy sorting match

    '''
    if matcherType == "WordWeight":
	return woreWeightMatch()
    elif matcherType == "Fuzzy":
	return fuzzyMatch(removeStopWords)
    elif matcherType == "bm25":
	return bm25()
    elif matcherType == "Vectorize":
	pass #TODO
    elif matcherType == "DeepLearning":
	pass #TODO
    else:
	print("[Error]: Invalided type.")
	exit()


def matcherTesting(matcherType, removeStopWords=False):
    
    matcher = getMatcher(matcherType, removeStopWords)
    while True:
	query = input("随便聊聊?: ")
	title, index = matcher.match(query)
	sim = matcher.getSimilarity()
	print("最为相似的标题是 %s, 相似度为 %d " % (title, sim))

	res = json.load(open(os.path.join("../knowledge_base/processed/reply/", str(int(index/1000))+'.json'), 'r', encoding='utf-8'))
	targetId = index % 1000
	
	evaluator = Evaluator()
	candidates = evaluator.getBestResponse(responses=res[targetId], topk=5, debugMode=False)
	print("以下是相似度前5的回复:") 
	for candidate in candidates:
	    print("%s %f" % (candidate[0], candidate[1]))


def woreWeightMatch():
    
    weightMatcher = WordWeightMatcher(segLib="jieba")
    weightMatcher.loadTitles(path="data/Titles.txt")
    weightMather.initialize()
    return weightMatcher


def fuzzyMatch(cleansw=False):
    fuzzyMatcher = FuzzyMatcher(segLib="jieba", removeStopWords=cleansw)
    fuzzyMatcher.loadTitles(path="../knowledge_base/Titles.txt")
    
    if cleansw:
	fuzzyMatcher.TitlesSegmentation(cleansw)
	fuzzyMatcher.joinTitles()

    return fuzzyMatcher


    #load a custom user dictionary.
    #fuzzyMatcher.TaibaCustomSetting(usr_dict="jieba_dictionary/ptt_dic.txt")

    #load stopwords
    #fuzzyMatcher.loadStopWords(path="data/stopwords/chinese_sw.txt")
    #fuzzyMatcher.loadStopWords(path="data/stopwords/ptt_words.txt")
    #fuzzyMatcher.loadStopWords(path="data/stopwords/specialMarks.txt")


def bm25():
    
    bm25Matcher = bestMatchingMatcher()
    bm25Matcher.loadTitle(path="../knolwdeg_base/Titles.txt")
    bm25Matcher.initilize()


if __name__ == '__main__':
    main()
