import pickle
import sys
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

"""

This is a quick way to check for similar links from the tf-idf matrix calculated by tf-idf.py
Usage is 'python check_link_similarity.py <link>'. Should be able to run this from node.js with
require('child_process'); Will test and find out more

"""

def find_similar(tfidf_matrix, index, top_n = 3):	
    cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
    return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]

def check_similarity(link, links):
	if(link in links):
		similar = find_similar(tfidf,links.index(link))
		for i in similar:
			print("\n%.2f%% similarity:\n" % (i[1]*100),links[i[0]])
		return(similar)
	else:
		return

tfidf = pickle.load(open("tfidf.pickle","rb"))
links = pickle.load(open("links.txt", "rb"))

link = sys.argv[1]

print("Checking for:\n %s" % link)
check_similarity(link, links)
