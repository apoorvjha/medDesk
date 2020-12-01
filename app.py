from flask import Flask,request,redirect,url_for,session,flash,render_template
import database
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename   # secured file upload
app=Flask(__name__)
app.secret_key='QwErTY9934@123'

@app.route('/')
def HomePage():
	return render_template('index.html')
@app.route('/register')
def register():
	return render_template('register.html')	
@app.route('/login')
def login():
	return render_template('login.html')
@app.route('/registerBack',methods=['POST'])
def registerBack():
	registrar=database.Registration()
	if request.method=='POST':
		userId=request.form['userId']
		password=sha256_crypt.encrypt(request.form['password'])
		email=request.form['email']
		profilePic=request.files['profilePic']
		fileName=userId + secure_filename(profilePic.filename)
		profilePic.save('/home/aj/Desktop/Tech/EduStartup/static/PROFILE_PIC/'+fileName)
	else:
		flash("Unsupported method of registration! Please use the registration tab instead.",'alert alert-danger')
		return redirect(url_for("HomePage"))
	profilePath='static/PROFILE_PIC/'+fileName
	res=registrar.registerUser(userId,password,email,profilePath)
	print(res)
	if res==True:
		# as we advance, incorporate functionality of OTP verification as well.
		flash("You are successfully registered! verification link has been sent to your registered E-mail.",'alert alert-success') 
		return redirect(url_for('login'))
	else:
		flash("User with provided data already exists! ",'alert alert-danger')
		return redirect(url_for('register'))

@app.route('/loginBack',methods=['POST'])
def loginBack():
	authenticator=database.AuthLogin()
	if request.method=='POST':
		userId=request.form['userId']
		password=request.form['password']
	else:
		flash("Unsupported method of login! Please use the login tab instead.",'alert alert-danger')
		return redirect(url_for("HomePage"))
	status,res,msg,category=authenticator.checkCredentials(userId,password)
	flash(msg,category)
	if status==True:
		session['username']=userId
		session['email']=res[0][2]
		session['profilePic']=res[0][3]
		session['type']=res[0][6]
		return redirect(url_for('HomePage'))
	else:
		return redirect(url_for('login'))

@app.route('/logout')
def logout():
	flash('You are successfully logged out!','alert alert-success')
	session.pop('username',None)
	session.pop('email',None)
	session.pop('profilePic',None)
	return redirect(url_for('HomePage'))
@app.route('/aboutus')
def aboutus():
	return render_template('aboutus.html')


@app.route('/contactus')
def contactus():
	return render_template('contactus.html')
@app.route('/admin')
def admin():
	return render_template('admin.html')
@app.route('/messenger')
def messenger():
	return render_template('messenger.html')
@app.route('/settings')
def settings():
	return render_template('settings.html')

@app.route('/ventures')
def ventures():
	return render_template('ventures.html')

@app.route('/activate')
def activate():
	otp = request.args.get('otp')
	userId=request.args.get('userId')
	otpVal=database.otpValidator()
	if otpVal.validate(otp,userId)==True:
		flash("Congratulations! Your account has been activated. Try logging in.",'alert alert-success')
		return redirect(url_for('login'))
	else:
		flash("OTP verification Failed! Try again later.")
		return redirect(url_for('HomePage'))


