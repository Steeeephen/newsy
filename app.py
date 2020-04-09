from __future__ import print_function
from flask import Flask, request, render_template, redirect
from pymongo import MongoClient

app = Flask(__name__, static_url_path='/static')

client = MongoClient("mongodb+srv://stephen:l98waDrJSyCUspzw@newsy-98fzw.mongodb.net/test?retryWrites=true&w=majority")


def new_user(form):
	login = client['newsy']['login']
	new_user_dict = {
		"firstname":form['firstname'],
		"lastname":form['lastname'],
		"password":form['password'], #to be encrypted
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
	password = user['password']
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
	value = { "$set": {"password":form['password']}}
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
