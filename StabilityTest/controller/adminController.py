from flask import Flask,url_for,g,session
from flask import render_template
from flask import request
from StabilityTest import app
from StabilityTest.dao import userDao

@app.route('/',methods=['GET','POST'])
def login(name=None):
	if request.method =='POST':
		username = request.form['username']
		password = request.form['password'] 
		if userDao.getUserPwd(username)==password :
			session['logged_in'] = True
			return render_template('admin-index.html')
		else:
			return render_template('login.html',name="error")
	else:
		print app.config['SECRET_KEY']
		return render_template('login.html')

@app.route('/admin',methods=['GET'])
def index():

	return render_template('admin-index.html')

@app.route('/shouye',methods=['GET'])
def shouye():

	return render_template('shouye.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return render_template('login.html')
