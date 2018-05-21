import json
import logging
import os

def main():
    filter = articleFilter()
    filter.load_processed_corpus()

    filter.print_titles()
    filter.print_response()


class articleFilter(object):
    def __init__(self):
        self.stopwords = None
        self.stoptags = None
	self.raw_data = None
	self.corpus = []
	self.order_response = []
	self.order_titles = []

	self.article_count = 0
	self.titles = set()
	self.users_info = {}
	self.init_load_stopwords()

	logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level = logging.INFO)
	
	
    def initLoadStopWords(self):
	'''
	
	'''
