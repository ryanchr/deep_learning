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
 	filter inappropriate responses	
	'''
	with open('../knowledge_base/stopwords/words.txt'. 'r', encoding='utf-8') as sw:
	    self.stopwords = [word.strip('\n') for word in sw]
	with open('../knowledge_Base/stopwords/gossiping.tag', 'r', encoding='utr-8') as sw:
	    self.stoptags = [word.strip('\n') for word in sw]

    def process_raw_data(self, path, is_dir=False, to_one_file=False, one_file_name="corpus.json"):
	data = []
	total = []
	filename = None
	count = 0

	if is_dir:
	    filenames = [name for name in os.listdir(path) if not name.startswith(".")]
	else:
	    filenames = [path]

	for filename in filenames:
	    count += 1
	    if count % 100 == 0:
		logging.info("已经处理 %d 页文章，其中有效文章数为 %d" % (count, self.article_count))
	    with open(os.path.join(path, filename), 'r', encoding="utf-8") as data:
		res = self.generate_corpus(json.load(data))

		if to_one_file:
		    total += res
		else:
		    with open("../knowledge_base/processed/"+filename, 'w', encoding='utf-8') as op:
			op.write(json.dumps(res, indent=4, ensure_ascii=False))
			logging.info("已处理 ” + filename)

	    if to_one_file:
		with open("../knowledge_base/processed/" + one_file_name, 'w', encoding='utf-8') as op":
		    op.write(json.dumps(total, indent=4, ensure_ascii=False))

    def reclean_corpus(self):
	pass


    def merge_corpuse(self, path="../knowledge_base/processed/"):
	logging.info("即将进行语料库的合并")
	corpus_names = [name for name in os.listdir(path))
		        if not name.startswith(".")
			and name != "reply"]
	all_corpus = []
	for corpus_name in corpus_names:
	    with open(os.path.join(path,corpus_name), 'r', encoding='utf-8') as data:
		c = json.load(data)
		logging.info("已经载入" + corpus_name)
		all_corpus += c
	with open("../knwoledge_base/processed/all_corpus.json", 'w', encoding='utf-8') as op:
	    op.write(json.dumps(all_corpus, indent=4, ensure_ascii=False))
	    logging.info)"合并文成，输出到 " + path + "all_corpus.json")

	
    def load_processed_corpus(self, path="data/processed/"):
	corpus_names = [name for name in os.listdir(path)
			if not name.startswith(".") and os.path.isfile(os.path.join("../knowledge_base/processed/",name))]
	logging.info("正在载入现有语料")
	for corpus_name in corpus_names:
	    with open(os.path.join(path,corpus_name), 'r', encoding='utf-8') as data:
		c = json.load(data)
		logging.info("已经载入 " + corpus_name)
		slef.corpus += c
		logging.info("并且读入了%d 篇文章" % len(self.corpus))

	logging.info("正在抽取文章与回复")
	
	for article in self.corpus:
		self.titles.add(article["Title"])
		self.order_titles.append(article["Title"])
		self.order_response.append(article["Responses"])
	logging.info("文章与回复提取完成")


    def generate_corpus(self, articles, drop_response=True, negative_tage=None, no_content=True, min_length=6):
	'''
	pick up articles based on corpus

	Args:
	    - articles: container of a posted article		
	    - drop_response: filter the reply or not
	    - negative_tag: tags to be filtered
	    - no_content: if save article content
	    - min_length: only save title length greater than min_length

	Return:
	    - corpus: a list of articles
	'''

	if negative_tag is None:
	    negative_tag = self.stoptags
	
	clean_article = []

	for article in articles:
	    ##filter unstructured articles
	    try:
		title = article["Title"]
		clean_responses = self.clean_responses(article["Responses"])
		if len(clean_responses) == 0:
		    continue
		article["responses"] = clean_responses
	    except Exception as e:
		continue

	    ##options for customized articles
	    if title in self.titles or len(title) < min_length:
		##filter article with short title or existed article
		continue
	    
	    if drop_response:
		##filter response article or forwarded article i.e. Re: and Fw:
		if title.startswith("Re") or title.startswith("Fw"):
		    continue

	    if no_content:
		article.pop("Content")

	    ##extract tags
	    tag, clean_title = self.get_tag(title) #separate title and tag
	    if tag in negative_tag: 
		continue
	
	    article["Tag"] = tag
	    article["Title"] = clean_title
	    self.titles.add(clean_title)
	    self.order_titles.append(clean_title)
	    self.order_reponse.append(clean_responses)

	    self.article_count += 1
	    clean_article.append(article)

	return clean_article


    def clean_responses(self, responses, negative_user=set(), min_length=6, stopwords=None):
	'''
	根据例子，回复长度和是否包含停用词来滤除消极的回复

	Args:
	    - responses: dictionary in the reply
	    - negative_user: user set used for filtering reply
	    - min_length: filter reply with length ssmaller than min_length
	    - stopwords: filter reply having sensitive words
	Return:
	    - responses: dictionary filtered negative reply
	'''

	if stopwords is None:
	    stopwords = self.stopwords

	clean_responses = []

	for response in responses:
	    drop = False
	   
	    ##filter replies from specific users
	    if response["User"] in negative_ser or len(response["Content"]) < min_length:
		drop = True
	    ##filter reply having stop words
	    for w in stopwords:
		if w in response["Content"]:
		    drop = True
	    if not drop:
		response["Content"] = response["Content"].strip()
		clean_response.append(response)

	return clean_responses

    
    def _update_users_history(self, response):
	'''
	record up vote or down vote
	'''
	user = response["User"]

	if user not in self.users_info.keys():
	    res = {
		"up" : 0,
		"down" : 0,
		"arrow" : 0
	    }
	    self.users_info[user] = res

	if response["Vote"] == "up":
	    self.users_info[user]["up"] += 1
	elif response["Vote"] == "down":
	    self.users_info[user]["down"] += 1
	else:
	    self.users_info[user]["arrow"] += 1


    def get_tage(self, title):
	'''
	return article tags and clean response
	'''

	try: 
	    tag, title = title.split("]", 1)
	except:
	    return None, title

	
    def print_titles(self):
	logging.info("正在输出文章标题")

	with open('../knowledge_base/Title.txt', 'w', encoding='utf-8') as op:
	    for title in self.order_titles:
		op.write(title + "\n")
	
	logging.info("文章标题输出完成“）


    def print_user_info(self):
	with open('../knowledge_base/User_info.txt', 'w', encoding='utf-8') as op:
	    op.write(json.dumps(self.users_info, indent=4, ensure_ascii=False))


    def print_reponse(self):
	logging.info("正在输出回复内容")
	resSplit = []
	sc = 0

	for response in self.order_response:
	    sc += 1
	    resSplit.append(response)
	    if sc % 1000 == 0:
		with open('../knowledge_base/processed/reply'+str(int(sc/1000)-1)+'.json', 'w', encoding='utf-8') as tr:
		    tr.write(json.dumps(resSplit, indent=4, ensure_ascii=False))
		    resSplit = []
		logging.info("已经输出 %d 篇回复" % sc) 
	logging.info("完成输出回复")


if __name__ == '__main__':
    main()




	

