import mysql.connector as mysql                    # for database communute.
import random
import quickstart
from passlib.hash import sha256_crypt
class DataBase:
	def __init__(self,credsFileName="credential.txt"):
		with open(credsFileName,'r') as authCred:
			self.credentials=authCred.read().split('\n')
	def dbServerlogin(self):
		con=mysql.connect(host=self.credentials[0],user=self.credentials[1],password=self.credentials[2],database=self.credentials[3])
     # connection setup with our database.

		return con
	def executeQuery(self,con,query,val=(),ReturnMode=True):
		myCursor=con.cursor()
		if ReturnMode==True:		
			myCursor.execute(query,val)
			res=myCursor.fetchall()
			return res
		else:
			myCursor.execute(query,val)
			con.commit()
			return

class AuthLogin:
	def __init__(self):
		self.db=DataBase()
		self.con=self.db.dbServerlogin()
	def checkCredentials(self,userId,password):
		query=f"SELECT * FROM `users` WHERE `Name`='{userId}'"
		res=self.db.executeQuery(self.con,query)
		stat,msg,category=self.checkActiveStatus(userId)
		if(len(res)!=0 and sha256_crypt.verify(password,res[0][1])):
			return stat,res,msg,category
		else:
			return False,None,"Incorrect login credentials, please try again! ",'alert alert-danger'
	def checkActiveStatus(self,userId):
		query=f"SELECT * FROM `users` WHERE `Name`='{userId}' AND `activeStatus`=1"
		res=self.db.executeQuery(self.con,query)
		if len(res)!=0:
			return True,"You are successfully logged in!",'alert alert-success'
		else:
			return False,"Your account is not active, complete E-mail verification to activate your account!",'alert alert-danger'
		
		
class Registration:
	def __init__(self):
		self.db=DataBase()
		self.con=self.db.dbServerlogin()
	def registerUser(self,userId,password,email,profilePic):
		query="INSERT INTO `users`(`Name`,`Password`,`Mail`,`ProfilePic`,`userType`) VALUES(%s,%s,%s,%s,'user')"
		query1="SELECT * FROM `users` WHERE `Name`=%s OR `Mail`=%s"
		val=(userId,password,email,profilePic)
		val1=(userId,email)
		res=self.db.executeQuery(self.con,query1,val1)
		if len(res)!=0:
			return False
		else:
			self.db.executeQuery(self.con,query,val,ReturnMode=False)
			self.verificationLinkGenerator(userId)
			return True
	def verificationLinkGenerator(self,userName):
		query=f"SELECT `userId`,`Mail` FROM `users` WHERE `Name`='{userName}'"
		res=self.db.executeQuery(self.con,query)
		otp=random.randint(100000,999999)
		userId=res[0][0]
		query2=f"INSERT INTO `activation` VALUES({userId},{otp})"
		self.db.executeQuery(self.con,query2,ReturnMode=False)
		message_text=f"127.0.0.1:5000/activate?otp={otp}&userId={userId}  is your link. Either click it or paste it into your browser. \n\n Thanks & Regards,\nMed-desk\n\n This is a system generated mail."
		quickstart.driver(senders_mail, res[0][1], "Account Verification", message_text)
		return
class otpValidator:
	def __init__(self):
		self.db=DataBase()
		self.con=self.db.dbServerlogin()
	def validate(self,otp,userId):
		query=f"SELECT * FROM `activation` WHERE `userId`={userId}"
		query1=f"UPDATE `users` SET `activeStatus`=1 WHERE `userId`={userId}"
		res=self.db.executeQuery(self.con,query)
		if(len(res)!=0):
			self.db.executeQuery(self.con,query1,ReturnMode=False)
			return True			
		else:
			return False
		
				
		
				
		
