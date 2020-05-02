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
from pymongo import MongoClient

"""

This takes the enabled RSS feeds directly from the database and builds tf-idf model which can be used
to check for similar articles in the database. We can periodically rerun this to keep it updated
Can be easily done with a 'watch' command from a linux terminal

Update: Not used in the final iteration of the site


"""


# Cleaning the article
def remove_url(text):
    url = re.compile(r'https?://\S+|www\.|pic\.\S+')
    text= url.sub(r'',text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation)) 
    text = re.split('\W+', text)
    text = [word for word in text if word not in stopword]
    text = ' '.join(text)
    return(text)

# Connect to the mongodb - pw would ideally not be stored in plain text 
client = MongoClient("mongodb+srv://stephen:l98waDrJSyCUspzw@newsy-98fzw.mongodb.net/test?retryWrites=true&w=majority")
newsy = client['newsy']
channel = newsy['Channel']
print("Connected to database")

# Find RSS feeds that are enabled
rss_links = channel.find({'enabled': {'$eq':True}})
urls = [""]*(channel.count_documents({'enabled': {'$eq':True}}))

print("Urls found:")
# Take their urls
for i,link in enumerate(rss_links):
	urls[i] = link['url']
	print(urls)

# Parse each feed
items = []
for url in urls:
	feed = feedparser.parse(url)
	items.extend(feed['items'][:10])
print("Feeds parsed")

links = [""]*len(items)
articles = [""]*len(items)

# Take articles and clean article text
for i in range(len(items)):	
	link = items[i]['link']
	x = requests.get(link)
	html = x.text
	links[i] = link
	soup = BeautifulSoup(html, 'lxml')
	try:
		article_text = soup.find_all('section', {'itemprop':'articleBody'})[0].get_text()
	except:	
		article_text = soup.find_all('div', {'class':'article-body'})[0].get_text()
	
	article_text = remove_url(article_text)
	articles[i] = article_text
print("Articles Cleaned")

tfidf_vec = TfidfVectorizer(use_idf=True)

tfidf = tfidf_vec.fit_transform(articles)

# Dump data to let similarity script use them
pickle.dump(links, open("links.txt","wb"))
pickle.dump(tfidf, open("tfidf.pickle", "wb"))
print("Tf-idf completed")