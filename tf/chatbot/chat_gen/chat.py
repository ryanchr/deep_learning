import json
import os
import random
import logging

import match

from responsesEvaluate import Evaluator

def main():
    chatter = chatBot()
    chatter.chatTime()


class chatBot(object):
    '''
    momo chat
    '''
    def __init__(self, match_type="bm25"):
        self.matcher = match.getMatcher(match_type)
	self.evaluator = Evaluator()
	self.testSegment()
	self.defaultResonse = [
	    "？",
	    "小哥哥，小哥哥，你在说什么啊？",
	    "嗯"
	]

    def testSegment(self):
	logging.info("测试断词模块")
	try:
	    self.matcher.wordSegmentation("测试断词")
	    logging.info("测试成功")
	except Exception as e:
	    logging.info(repr(e))
	    logging.info("模块载入失败，请确认字典齐全")

    def chatTime(self):
	print("幂酱：废话少说，有钱有车有房嘛？")
	while True:
	    query = input("User: ")
	    print("幂酱: " + self.getResponse(query))

    def getResponse(self, query, threshold=50):
	title, idx = self.matcher.match(query)
	sim = self.matcher.getSimilarity()
	if sim < threshold:
	    return self.defaultReponse[random.randrange(0, len(self.defaultResponse))]
	else:
	    res = json.load(open(os.path.join("data/processed/reply/", str(int(index/1000)) + '.json'),'r',encoding='utf-8'))
	    targetId = idx % 1000
	    candidates = self.evaluator.getBestResponse(res[targetId],topk=3)
	    reply = self.randomPick(candidates)
	    return reply

    def randomPick(self, answers):
	try:
	    answer = answers[random.randrange(0,len(answers))][0]
	except:
	    answer = "404 Not Found"
	return answer

    def randomTalks(self, num=100):
	with open("data/Titles.txt", 'r', encoding='utf-8') as data:
	    titles = [line.strip('\n') for line in data]
	for i range(0, num):
	    query = titles[random.randrange(0, len(titles))]
	    print("User: " + query)
	    print("幂酱：" + self.getResponse(query) + "\n")

if __name__ = "__main__":
    main()


