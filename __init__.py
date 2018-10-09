from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_wtf import FlaskForm
from flask_pymongo import PyMongo
from wtforms import TextField, PasswordField, BooleanField, SubmitField
from pymongo import MongoClient
from wtforms.validators import InputRequired, Length, DataRequired
import random

name = ''
rand = ''

app = Flask(__name__)
app.config['SECRET_KEY']= 'TheMainFile'
client = MongoClient("mongodb://priki:priki123@ds121673.mlab.com:21673/url")
db = client.get_database('url')
url_record = db.url_record

class LoginForm(FlaskForm):
	username = TextField('username', validators=[DataRequired(), Length(max=9)])
	password = PasswordField('password', validators=[DataRequired()])
	submit = SubmitField('Submit')
	urls = TextField('urls')

class SignupForm(FlaskForm):
	username = TextField('username', validators=[DataRequired(), Length(max=9)])
	password = PasswordField('password', validators=[DataRequired()])
	# submit = SubmitField('submit')
	urls = TextField('urls')


@app.route('/', methods=['POST','GET'])
def login():
	loginForm = LoginForm()
	signupForm = SignupForm()

	url_record = db.url_record
	session['username'] = None

	msg = 'Invalid Username or Password'
	if request.method == 'POST':
		if loginForm.submit.data and loginForm.validate_on_submit:
			print("asd")
			search = url_record.find_one({'username':loginForm.username.data})
			if search is None:
				return render_template('login.html', msg=msg, loginForm=loginForm, signupForm=signupForm)
				
			authu = search['username']
			authp = search['password']
			if authu == loginForm.username.data and authp == loginForm.password.data:
				session['username'] = loginForm.username.data
				return redirect(url_for('url', name=authu))
			
			return render_template('login.html', msg=msg, loginForm=loginForm, signupForm=signupForm)

		elif signupForm.validate_on_submit:
			search = url_record.find_one({'username':signupForm.username.data})
			if search:
				msg = 'Username already exists'
				return redirect(url_for('login'))
			else:
				url_record.insert({'username':signupForm.username.data,'password':signupForm.password.data})
				return redirect(url_for('login'))

	return render_template('login.html', loginForm=loginForm, signupForm=signupForm)

@app.route('/<name>', methods=['POST','GET'])
def url(name):
	form = LoginForm()
	urls = db[name]
	msg = None
	if session['username']:
		if request.method == 'POST':
			search = urls.find_one({'real':form.urls.data})
			if search:
				msg = 'URL already shortned'
				flash(msg)
				return redirect(url_for('url', name=name))
			else:
				rand = random.randint(0, pow(10, 5))
				temp = "http://127.0.0.1:5000/"+name+"/"+ str(rand)
				urls.insert({'real':form.urls.data,'short':temp})
				return redirect(url_for('url', name=name))

		else:
			hi = urls.find()
			return render_template('shortner.html', form=form, name=name, hi=hi)

	return redirect(url_for('login'))

@app.route('/<name>/<trunc>', methods=['POST','GET'])
def link(name,trunc): 
	urls = db[name]
	search = urls.find_one({'short':'http://127.0.0.1:5000/'+name+'/'+trunc})
	if search:
		return redirect(search['real'])
	return redirect(url_for('url', name=name))

@app.route('/logout')
def logout():
	session['username'] = None
	return redirect(url_for('login'))


if __name__ == '__main__':
	app.secret_key= 'TheMainFile'
	app.run(debug=True)
