from flask import Flask, request, render_template
app = Flask(__name__, static_url_path='/static')

@app.route('/')
@app.route('/register')
def home():
    return render_template('index.html', title = "Newsy")

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/forgotpass')
def forgot_pw():
	return render_template('forgotpass.html')

@app.route('/resetpass')
def resetpw():
	return render_template('resetpass.html')

if __name__ == "__main__":
    app.run(debug=True)
