from .import Matcher

class KeywWordMatcher(Matcher):

    '''
    compare similarity of phrases using TF-IDF
    '''

    def __init__(self):
	self.vecModel = None
	
    def match(self, query):
	pass	

