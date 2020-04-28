from __future__ import print_function
from flask import Flask, request, render_template, redirect, Markup
from pymongo import MongoClient
from Crypto.Cipher import AES
from Crypto import Random
import os
import base64
import hashlib
import feedparser

app = Flask(__name__, static_url_path='/static')

client = MongoClient("mongodb+srv://stephen:l98waDrJSyCUspzw@newsy-98fzw.mongodb.net/test?retryWrites=true&w=majority")

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
 
key = "G8UWRgVYsAzJJZpArEEMbkg7srftxtCGxVf2Vs9RecxJE52bJUhpx8GpNHAjbYj3pnt7tEeKvGRn3Q7RQutceZL9sHcgBssqjzxAz82u6HwsBdNfhbVFdpHURySqvC2eAJE9emf6pvdFZ3F7KLwXaJAFwYjZMRFBhGN3x7EacnXxaKvZas8MsUQGMK9pS6ERVt5Xcx4BeqwNRaMBTXygYrpwrkN93VdDDDJqH86rWvjj8AQsVMjhjvDWMVnUGKt6"
 
def encrypt(raw, key):
	private_key = hashlib.sha256(key.encode("utf-8")).digest()
	raw = pad(raw)
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(private_key, AES.MODE_CBC, iv)
	return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, raw):
	private_key = hashlib.sha256(key.encode("utf-8")).digest()
	enc = base64.b64decode(enc)
	enc = base64.b64decode(enc)
	iv = enc[:16]
	cipher = AES.new(private_key, AES.MODE_CBC, iv)
	return unpad(cipher.decrypt(enc[16:])).decode("utf-8")

def new_user(form):
	login = client['newsy']['login']
	new_user_dict = {
		"firstname":form['firstname'],
		"lastname":form['lastname'],
		"password":base64.b64encode(encrypt(form['password'],key)).decode("utf8"), #to be encrypted
		"gender":form['gender'],
		"email":form['email'],
		"phone":form['phone'],
		"question":form['question'],
		"answer":form['answer'],
		"editor":form['editor']=="True"
	}
	login.insert_one(new_user_dict)

def check_login(form):
	login = client['newsy']['login']
	user = login.find_one({'email': {'$eq': form['email']}})
	password = decrypt(user['password'],key)
	return password == form['password']

def check_reset(form):
	login = client['newsy']['login']
	user = login.find_one({'email': {'$eq': form['email']}})
	question = user['question']
	answer = user['answer']
	print(question, answer, form['question'], form['answer'])
	return question == form['question'] and answer == form['answer']

def reset_password(form):
	login = client['newsy']['login']
	query = {"email":form['email']}
	value = { "$set": {"password":encrypt(form['password'],key)}}
	login.update_one(query, value)

# Initial registration page
@app.route('/', methods = ['GET','POST'])
@app.route('/register', methods = ['GET','POST'])
def home():
	if(request.method == "POST"):
		new_user(request.form) #need to verify fully
		return 'main page goes here' #to add
	else:
		return render_template('index.html', title = "Newsy")

# Login page
@app.route('/login',methods = ['GET','POST'])
def login():
	if(request.method == "POST"):
		if(check_login(request.form)):
			return redirect('home')
		else:
			return redirect('login')
	else:
		return render_template('login.html', title = "Newsy")

# Forgot password page
@app.route('/forgotpass', methods=['GET','POST'])
def forgot_pw():
	if(request.method == "POST"):
		if(check_reset(request.form)):
			return redirect('resetpass')
		else:
			return redirect('forgotpass')
	else:
		return render_template('forgotpass.html', title = "Newsy")

# Reset password page
@app.route('/resetpass', methods=['GET','POST'])
def resetpw():
	if(request.method == "POST"):
		reset_password(request.form)
		return 'password change success' #to add
	else:
		return render_template('resetpass.html', title = "Newsy")

@app.route('/home', methods=['GET','POST'])
def homepage():
	url_list = [i['url'] for i in client.newsy.Channel.find({'enabled': {'$eq': True}})]
	print(url_list)

	thumbnails = []
	titles = []
	actuallinks = []
	for url in url_list:
		feed = feedparser.parse(url)
		for i in range(10):
			thumbnails.append(feed['items'][i]['media_thumbnail'])
			titles.append(feed['items'][i]['title'])
			actuallinks.append(feed['items'][i]['link'])
	
	for i in range(len(actuallinks)):
		query = {'url':actuallinks[i]}
		newval = {'$set': {'url': actuallinks[i], 'image': thumbnails[i], 'title':titles[i]}}
		client.newsy.articles.update(query, newval, True)

	article_format = """
	<li class="col-4">
						<div class="card">
							<img src="{0}" class="card-img-top" alt="...">
							<div class="card-body">
								<h5 class="card-title">{1}</h5>
								<a href="/clicked/{2}" target = "_blank" class="btn btn-primary">Click</a>
							</div>
						</div>
					</li>
	"""
	article_html = ""
	for i in range(len(thumbnails)):
		article_html += article_format.format(thumbnails[i],titles[i],actuallinks[i].replace("/","€€€€€"))

	topic_list = [i['topic'] for i  in client.newsy.topics.find({})]
	topic_format = """
	<li class="list-group-item">
					<div class="row">
						<div class="col-9" onclick = "location.href='topic/{0}'" type="button">{0}</div>
						<button type="button" onclick = "location.href='/removetopic/{0}'" class="btn btn-outline-dark btn-sm col-3">
						X
					</button>
					</div>
				</li>
	"""
	topic_html = ""
	for i in topic_list:
		topic_html += topic_format.format(i)

	channel_list = [i['name'] for i in client.newsy.Channel.find({'enabled': {'$eq': True}})]
	channel_format = """
	<li class="list-group-item " type="button">
					<div class="row">
						<div class="col-9">{0}</div>
						<button type="button" onclick = "location.href='/enablechannel/{0}'" class="btn btn-primary col-3">
						Edit
					</button>
					</div>
				</li>
	"""
	channel_html = ""
	for i in channel_list:
		channel_html += channel_format.format(i)
	return render_template('home.html', topic = Markup(topic_html), channels = Markup(channel_html), articles = Markup(article_html))

@app.route('/topic/<topic_keyword>', methods=['GET','POST'])
def topicpage(topic_keyword):
	if "AND" in topic_keyword:
		compound = True
		keywords = topic_keyword.replace(" ", "").split("AND")
	else:
		compound = False
		keywords = topic_keyword.split(" ")
	
	topic_list = [i['topic'] for i  in client.newsy.topics.find({})]
	
	topic_format = """
	<li class="list-group-item">
					<div class="row">
						<div class="col-9" onclick = "location.href='{0}'" type="button">{0}</div>
						<button type="button" onclick = "location.href='/removetopic/{0}'" class="btn btn-outline-dark btn-sm col-3">
						X
					</button>
					</div>
				</li>
	"""
	topic_html = ""
	for i in topic_list:
		topic_html += topic_format.format(i)

	channel_list = [i['name'] for i in client.newsy.Channel.find({'enabled': {'$eq': True}})]
	channel_format = """
	<li class="list-group-item " type="button">
					<div class="row">
						<div class="col-9">{0}</div>
						<button type="button" onclick = "location.href='/enablechannel/{0}'" class="btn btn-primary col-3" >
						Enable
					</button>
					</div>
				</li>
	"""
	channel_html = ""
	for i in channel_list:
		channel_html += channel_format.format(i)

	article_format = """
	<li class="col-4">
						<div class="card">
							<img src="{0}" class="card-img-top" alt="...">
							<div class="card-body">
								<h5 class="card-title">{1}</h5>
								<a href="/clicked/{2}" target = "_blank" class="btn btn-primary">Click</a>
							</div>
						</div>
					</li>
	"""
	article_html = ""

	titles = []
	thumbnails = []
	actuallinks = []
	if compound:
		reg = "%s" + "|%s"*(len(keywords)-1) + ".*"
		reg2 = ".*" + reg*(len(keywords))
		extended = []
		for i in range(len(keywords)):
			extended.extend(keywords)
		for article in client.newsy.articles.find({'title': {'$regex': reg2 % tuple(extended), '$options': 'i'}}):
				actuallinks.append(article['url'])
				thumbnails.append(article['image'])
				titles.append(article['title'])
	else:
		for keyword in keywords:
			for article in client.newsy.articles.find({'title': {'$regex': ".*%s.*" % keyword, '$options': 'i'}}):
				actuallinks.append(article['url'])
				thumbnails.append(article['image'])
				titles.append(article['title'])
	
	for i in range(len(thumbnails)):
		article_html += article_format.format(thumbnails[i],titles[i],actuallinks[i].replace("/","€€€€€"))

	return render_template('home.html', topic = Markup(topic_html),channels = Markup(channel_html), articles = Markup(article_html))

@app.route('/addtopic', methods = ['POST'])
def addtopic():
	client.newsy.topics.insert_one({'topic':request.form['topic']})
	return redirect('/home')


@app.route('/addchannel', methods = ['POST'])
def addchannel():
	client.newsy.Channel.insert_one({
		'name':request.form['name'],
		'url':request.form['url'],
		'enabled':True})
	return redirect('/home')

@app.route('/removetopic/<remove_topic>')
def removetopic(remove_topic):
	client.newsy.topics.delete_one({'topic':remove_topic})
	return redirect('/home')

@app.route('/enablechannel/<enable_channel>')
def enablechannel(enable_channel):
	query = {"name":enable_channel}
	value = { "$set": {"enabled":False}}
	client.newsy.Channel.update_one(query, value)
	return redirect('/home')

@app.route('/clicked/<link>')
def clicklink(link):
	link = link.replace("€€€€€","/")
	query = {'url': {'$regex': '.*%s.*' % link}}
	newval = {'$inc': {'count':1}}
	client.newsy.articles.update(query,newval, True)
	return redirect(link)

if __name__ == "__main__":
	app.run(debug=True)
