from flask import Flask, url_for, redirect, request,render_template
from flask_mysqldb import MySQL
import hashlib

app = Flask(__name__)
mysql = MySQL(app)
#m = hashlib.md5()

@app.route('/sign-up',methods = ['POST', 'GET'])
def signup():
   	if request.method == 'POST':
		first = request.form['first']
		last = request.form['last']
		email = request.form['email']
		pwd = request.form['pwd']
		rpwd = request.form['rpwd']
		date = request.form['date']
		month = request.form['month']
		year = request.form['year']
		gender = request.form['gender']
		phone = request.form['phone']
		dlno = request.form['dlno']
		door = request.form['doorNo']
		street = request.form['streetName']
		city = request.form['city']
		state = request.form['state']
		if(pwd != rpwd):
			return render_template("sign-up(1).html",flag = 1)
		m = hashlib.md5()	
		m.update(pwd)
		phash = m.hexdigest()
		#print "INSERT INTO Customer values(1,'"+first+" "+last+"',"+year+month+date+",'"+phone+"','"+phash+"','"+dlno+"', 10,'MG Road','Bangalore','Karnataka',NULL);"
		con = mysql.connection
		cur = con.cursor()
		cur.execute("Use car_rental;")
		cur.execute("INSERT INTO Customer(C_name,DoB,Phone,Password_hash,DL_Number,Door_Number,Street_Name,City,State) values('"+first+" "+last+"',"+year+month+date+",'"+phone+"','"+phash+"','"+dlno+"',"+door+",'"+street+"','"+city+"','"+state+"');")
		con.commit()
		return "Success"
  	#else:
      	#	user = request.args.get('nm')
    	#return redirect(url_for('success',name = user))


@app.route('/login',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		email = request.form['phone']
		password = request.form['password']
		con = mysql.connection
		cur = con.cursor()
		cur.execute("Use car_rental;")
		cur.execute("Select Password_hash from Customer where Phone = '"+email+"';")
		data = cur.fetchall()
		print data[0]
		m = hashlib.md5()
		m.update(password)
		phash = m.hexdigest()
		print "\n" + phash
		if(phash == data[0][0]):
			return "Success"
		else:
			return "Fail"
		

if __name__ == '__main__':
   app.run(debug = True)
