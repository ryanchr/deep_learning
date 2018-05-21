import os
import json

from gensim import corpora
from article import Article

class Corpus(object):
    def __init__(self):
	self.corpus = []
	pass

class webCorpus(Corpus):

    def __init(self):
	self.corpus = []

    def load_data(self, path, is_dir=False):
	
	data = []
	fileName = None

	if is_dir:
	    fileNames = [name for name in os.listdir(path) if not name.startswith(".")]
	else:
	    fileNames = [path]
	
	for fileName in fileNames:
	    with open(os.path.join(path, fileName), 'r', encoding="utf-8") as data:
		tp = json.load(data)
		for article in tp:
		    try:
			self.corpus.append(Article(article))
		    except:
			print("文章解析出错" + fileName)

    def get_text(self):
	for article in self.corpus:
	 
	    title = article.title
	    resp = ""
	    for r in article.responses:
		resp += ' ' + r["Content"]
	    yield title + resp

    def get_titles(self):
	for article in self.corpus:
	    yield article.title

