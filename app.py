from __future__ import print_function
from flask import Flask, request, render_template, redirect, Markup
import flask_login
from pymongo import MongoClient
from Crypto.Cipher import AES
from Crypto import Random
import os
import base64
import hashlib
import feedparser

app = Flask(__name__, static_url_path='/static')

login_manager = flask_login.LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)

client = MongoClient("mongodb+srv://stephen:l98waDrJSyCUspzw@newsy-98fzw.mongodb.net/test?retryWrites=true&w=majority")

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
 
class User(flask_login.UserMixin):
	pass

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return 'Logged out'


app.secret_key = "G8UWRgVYsAzJJZpArEEMbkg7srftxtCGxVf2Vs9RecxJE52bJUhpx8GpNHAjbYj3pnt7tEeKvGRn3Q7RQutceZL9sHcgBssqjzxAz82u6HwsBdNfhbVFdpHURySqvC2eAJE9emf6pvdFZ3F7KLwXaJAFwYjZMRFBhGN3x7EacnXxaKvZas8MsUQGMK9pS6ERVt5Xcx4BeqwNRaMBTXygYrpwrkN93VdDDDJqH86rWvjj8AQsVMjhjvDWMVnUGKt6"
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
		return redirect('login')
	else:
		return render_template('index.html', title = "Newsy")

# Login page
@app.route('/login',methods = ['GET','POST'])
def login():
	if(request.method == "POST"):
		if(check_login(request.form)):
			user = User()
			user.id = request.form['email']
			flask_login.login_user(user)
			print("logged in")
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
@flask_login.login_required
def homepage():
	editor_logged = (client.newsy.login.find_one({'email': {'$eq': flask_login.current_user.id}})['editor'])
	url_list = [i['url'] for i in client.newsy.Channel.find({'enabled': {'$eq': True}})]
	print(url_list)

	thumbnails = []
	titles = []
	actuallinks = []
	for url in url_list:
		feed = feedparser.parse(url)
		for i in range(10):
			try:
				thumbnails.append(feed['items'][i]['media_content'][0]['url'])
			except:
				thumbnails.append('')
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
	if(editor_logged):
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
	else:
		topic_format = """
		<li class="list-group-item">
						<div class="row">
							<div class="col-9" onclick = "location.href='topic/{0}'" type="button">{0}</div>
							</div>
					</li>
		"""
	topic_html = ""
	for i in topic_list:
		topic_html += topic_format.format(i)

	channel_list = [i['name'] for i in client.newsy.Channel.find({'enabled': {'$eq': True}})]
	if(editor_logged):
		channel_format = """
		<li class="list-group-item " type="button">
						<div class="row">
							<div class="col-9">{0}</div>
							<button type="button" onclick = "location.href='/enablechannel/{0}'" class="btn btn-primary col-3">
							Toggle
						</button>
						</div>
					</li>
		"""
		add_button_channel = """
		<button type="button" class="btn col-3" data-toggle="modal" data-target="#addChannelModal">Add</button>
		"""
		add_button_topic = """
		<button type="button" class="btn col-3" data-toggle="modal" data-target="#addTopicModal">Add</button>
		"""
	else:
		channel_format = """
		<li class="list-group-item " type="button">
						<div class="row">
							<div class="col-9">{0}</div>
						</div>
					</li>
		"""
		add_button_channel = ""
		add_button_topic = ""

	channel_html = ""
	for i in channel_list:
		channel_html += channel_format.format(i)
	return render_template('home.html', 
		topic = Markup(topic_html), 
		channels = Markup(channel_html), 
		articles = Markup(article_html),
		add_button_channel = Markup(add_button_channel),
		add_button_topic = Markup(add_button_topic))


@app.route('/topic/<topic_keyword>', methods=['GET','POST'])
@flask_login.login_required
def topicpage(topic_keyword):
	editor_logged = (client.newsy.login.find_one({'email': {'$eq': flask_login.current_user.id}})['editor'])
	if "AND" in topic_keyword:
		compound = True
		keywords = topic_keyword.replace(" ", "").split("AND")
	else:
		compound = False
		keywords = topic_keyword.split(" ")
	
	topic_list = [i['topic'] for i  in client.newsy.topics.find({})]
	
	if(editor_logged):
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
	else:
		topic_format = """
		<li class="list-group-item">
						<div class="row">
							<div class="col-9" onclick = "location.href='{0}'" type="button">{0}</div>
							</div>
					</li>
		"""
	topic_html = ""
	for i in topic_list:
		topic_html += topic_format.format(i)

	channel_list = [i['name'] for i in client.newsy.Channel.find({'enabled': {'$eq': True}})]
	if(editor_logged):
		channel_format = """
		<li class="list-group-item " type="button">
						<div class="row">
							<div class="col-9">{0}</div>
							<button type="button" onclick = "location.href='/enablechannel/{0}'" class="btn btn-primary col-3">
							Toggle
						</button>
						</div>
					</li>
		"""
		add_button_channel = """
		<button type="button" class="btn col-3" data-toggle="modal" data-target="#addChannelModal">Add</button>
		"""
		add_button_topic = """
		<button type="button" class="btn col-3" data-toggle="modal" data-target="#addTopicModal">Add</button>
		"""
	else:
		channel_format = """
		<li class="list-group-item " type="button">
						<div class="row">
							<div class="col-9">{0}</div>
						</div>
					</li>
		"""
		add_button_channel = ""
		add_button_topic = ""

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

	return render_template('home.html', 
		topic = Markup(topic_html), 
		channels = Markup(channel_html), 
		articles = Markup(article_html),
		add_button_channel = Markup(add_button_channel),
		add_button_topic = Markup(add_button_topic))

@app.route('/addtopic', methods = ['POST'])
@flask_login.login_required
def addtopic():
	client.newsy.topics.insert_one({'topic':request.form['topic']})
	return redirect('/home')


@app.route('/addchannel', methods = ['POST'])
@flask_login.login_required
def addchannel():
	client.newsy.Channel.insert_one({
		'name':request.form['name'],
		'url':request.form['url'],
		'enabled':True})
	return redirect('/home')

@app.route('/removetopic/<remove_topic>')
@flask_login.login_required
def removetopic(remove_topic):
	client.newsy.topics.delete_one({'topic':remove_topic})
	return redirect('/home')

@app.route('/enablechannel/<enable_channel>')
@flask_login.login_required
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


@login_manager.user_loader
def user_loader(email):
	emails = []
	for i in (client.newsy.login.find({})):
		emails.append(i['email'])
	print(emails)
	if email not in emails:
		return
	user = User()
	user.id = email
	return user

@login_manager.request_loader
def request_loader(request):
	print(request)
	email = request.form.get('email')
	
	emails = []
	for i in (client.newsy.login.find({})):
		emails.append(i['email'])
	print(emails)
	if email not in emails:
		print("ok")
		return

	#users = [email]
	#if email not in users:
	#   return

	user = User()
	user.id = email

	#user.is_authenticated = request.form['password'] == users[email]['password']

	return user


if __name__ == "__main__":
	app.run(debug=True)

