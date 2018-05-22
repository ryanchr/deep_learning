class QuickSearcher(object):
    '''
    build mapping for words in each sentence
    '''

    def __init__(self, docs=None):
        self.inverted_word_dic = dict()

    def buildInvertedIndex(self, docs):
        '''
        build reversely sorted index for id
        
        Args:
            - docs: docs to be sorted
        '''

        for docId, doc in enumerate(docs):
            for word in doc:
                if word not in self.inverted_word_dic.keys()
                    self.inverted_word_dic[word] = set()
                self.inverted_word_dic[word].add(docId)


    def quickSearch(self, query):
        '''
        read segmented query, get ids based on index
        '''
        result = set()
        for word in query:
            if word in self.inverted_word_dic.keys():
                result = result.union(self.inverted_word_dic[word])

        return result

