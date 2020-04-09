from __future__ import print_function
from flask import Flask, request, render_template, redirect

app = Flask(__name__, static_url_path='/static')


@app.route('/', methods = ['GET','POST'])
@app.route('/register', methods = ['GET','POST'])
def home():
	if(request.method == "POST"):
		print(request.form)
		return 'main page goes here' #to add
	else:
		return render_template('index.html', title = "Newsy")

@app.route('/login',methods = ['GET','POST'])
def login():
	if(request.method == "POST"):
		print(request.form)
		return 'main page goes here' #to add
	else:
		return render_template('login.html', title = "Newsy")

@app.route('/forgotpass', methods=['GET','POST'])
def forgot_pw():
	if(request.method == "POST"):
		print(request.form)
		return redirect('resetpass')
	else:
		return render_template('forgotpass.html', title = "Newsy")

@app.route('/resetpass', methods=['GET','POST'])
def resetpw():
	if(request.method == "POST"):
		print(request.form)
		return 'password change success' #to add
	else:
		return render_template('resetpass.html', title = "Newsy")

if __name__ == "__main__":
	app.run(debug=True)
