from bs4 import BeautifulSoup
import requests
import nltk
import string
import re
import feedparser
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer
stopword = nltk.corpus.stopwords.words('english')
import pickle
import time
from sklearn.metrics.pairwise import linear_kernel

def find_similar(tfidf_matrix, index, top_n = 3):	
    cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
    return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]

t1 = time.time()

def remove_url(text):
    url = re.compile(r'https?://\S+|www\.|pic\.\S+')
    text= url.sub(r'',text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation)) 
    text = re.split('\W+', text)
    text = [word for word in text if word not in stopword]
    text = ' '.join(text)
    return(text)

urls = ["https://rss.nytimes.com/services/xml/rss/nyt/Soccer.xml",
		"https://rss.nytimes.com/services/xml/rss/nyt/CollegeFootball.xml",
		"https://rss.nytimes.com/services/xml/rss/nyt/Hockey.xml"]

items = []
for url in urls:
	feed = feedparser.parse(url)
	items.extend(feed['items'])

links = [""]*len(items)

articles = [""]*len(items)

for i in range(len(items)):	
	link = items[i]['link']
	x = requests.get(link)
	html = x.text
	links[i] = link
	soup = BeautifulSoup(html, 'lxml')
	article_text = soup.find_all('section', {'itemprop':'articleBody'})[0].get_text()
	article_text = remove_url(article_text)
	articles[i] = article_text


tfidf_vec = TfidfVectorizer(use_idf=True)

tfidf = tfidf_vec.fit_transform(articles)

pickle.dump(links, open("links.txt","wb"))
pickle.dump(tfidf, open("tfidf.pickle", "wb"))


print("Checking for:\n %s" % links[-1])
similar = find_similar(tfidf,len(links)-1)

for i in similar:
	print("\n%.2f%% similarity:\n" % (i[1]*100),links[i[0]])

print(time.time() - t1)