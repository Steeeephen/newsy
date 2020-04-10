from __future__ import print_function
from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
from Crypto.Cipher import AES
from Crypto import Random
import os
import base64
import hashlib


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
			return 'main page goes here' #to add
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


if __name__ == "__main__":
	app.run(debug=True)
