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
		return redirect(url_for('login'))
  	else:
    		return render_template("sign-up(1).html",flag = 0)


@app.route('/login',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		phone = request.form['phone']
		password = request.form['password']
		con = mysql.connection
		cur = con.cursor()
		cur.execute("Use car_rental;")
		cur.execute("Select Password_hash,C_ID from Customer where Phone = '"+phone+"';")
		data = cur.fetchall()
		#print data[0]
		m = hashlib.md5()
		m.update(password)
		phash = m.hexdigest()
		#print "\n" + phash
		if(phash == data[0][0]):
			if(phone == "0"):
				return redirect(url_for('admin',flag = 0))
			else:
				return redirect(url_for('home',user = data[0][1]))
		else:
			return render_template("login.html",flag = 1)
	else:
		return render_template("login.html",flag = 0)
@app.route('/home/<int:user>')
def home(user):
	con = mysql.connection
	cur = con.cursor()
	cur.execute("Use car_rental;")
	cur.execute("Select Password_hash,C_Name from Customer where C_ID = "+str(user)+";")
	data = cur.fetchall()
	return render_template("home-1.html",name = data[0][1])

@app.route('/forgotpassword')
def fpwd():
	return render_template('forgotpassword.html')

@app.route('/contact-us')
def contact():
	return render_template('contact-us.html')

@app.route('/recovery')
def recover():
	return render_template('recovery.html')
@app.route('/booking/<user>',methods = ['POST'])
def booking(user):
	location = request.form['city']
	pickup = request.form['pickup']
	dropoff = request.form['dropoff']
	con = mysql.connection
	cur = con.cursor()
	cur.execute("Use car_rental;")
	cur.execute("select Registration_Number,Location,Car_Model, Car_Company, No_of_Seats,Weekday_Rates, Weekend_Rates,Peak_Season_Rates from Car_Details INNER JOIN Car_Type t using (Car_Model) where Registration_Number NOT IN (Select Registration_Number from Billing)and Location='"+location+"' UNION select Registration_Number,Location, Car_Model, Car_Company, No_of_Seats,Weekday_Rates,Weekend_Rates,Peak_Season_Rates from Car_Details c INNER JOIN Billing b using(Registration_Number) INNER JOIN Car_Type t using (Car_Model) where c.Location='"+location+"' and Booking_Date not between '"+pickup+"' and '"+dropoff+"' and DATE_ADD(Booking_Date,INTERVAL Booking_Duration DAY) not between '"+pickup+"' and '"+dropoff+"';")	
	
	data = cur.fetchall()
	cur.execute("select Chauffeur_ID, Chauffeur_Name, Per_Hour_Charges from Chauffeur c INNER JOIN Billing b using(Chauffeur_ID) where b.Booking_Date NOT BETWEEN '"+pickup+"' and '"+dropoff+"' and DATE_ADD(b.Booking_Date,INTERVAL b.Booking_Duration DAY) not between '"+pickup+"' and '"+dropoff+"' and  c.location='"+location+"' UNION select Chauffeur_ID,Chauffeur_Name,Per_Hour_Charges from Chauffeur where Chauffeur_ID not in(select Chauffeur_ID from Billing where Chauffeur_ID is not null) and location='"+location+"';");
	data2 = cur.fetchall()

	return render_template("booking.html",location = location, pick_up = pickup, drop_off = dropoff, items = data,items2 = data2)

@app.route('/ritz')
def ritz():
	con = mysql.connection
	cur = con.cursor()
	cur.execute("Use car_rental;")
	cur.execute("Select * from Car_Type where Car_Model like 'Ritz';")
	data = cur.fetchall()
	return render_template("ritz.html",item = data[0])

@app.route('/swift')
def swift():
	con = mysql.connection
	cur = con.cursor()
	cur.execute("Use car_rental;")
	cur.execute("Select * from Car_Type where Car_Model like 'Swift';")
	data = cur.fetchall()
	return render_template("swift.html",item = data[0])

@app.route('/scorpio')
def scorpio():
	con = mysql.connection
	cur = con.cursor()
	cur.execute("Use car_rental;")
	cur.execute("Select * from Car_Type where Car_Model like 'Scorpio';")
	data = cur.fetchall()
	return render_template("scorpio.html",item = data[0])

@app.route('/innova')
def innova():
	con = mysql.connection
	cur = con.cursor()
	cur.execute("Use car_rental;")
	cur.execute("Select * from Car_Type where Car_Model like 'Innova';")
	data = cur.fetchall()
	return render_template("innova.html",item = data[0])

@app.route('/admin',methods = ['GET','POST'])
def admin():
	if request.method =='POST':
		if request.form['submit'] == "Add Car":
			return render_template('admin.html',flag = 1)
		elif request.form['submit'] == "Remove Car":
			return render_template('admin.html',flag = 2)
		elif request.form['submit'] == "Modify Car":
			return render_template('admin.html',flag = 3)
		elif request.form['submit'] == "Remove Customer":
			return render_template('admin.html',flag = 4)
		elif request.form['submit'] == "Modify Customer":
			return render_template('admin.html',flag = 5)
		elif request.form['submit'] == "Add Chauffeur":
			return render_template('admin.html',flag = 6)
		elif request.form['submit'] == "Remove Chauffeur":
			return render_template('admin.html',flag = 7)
		elif request.form['submit'] == "Modify Chauffeur":
			return render_template('admin.html',flag = 8)
		elif request.form['submit'] == "Car Add":
			deposit = request.form['deposit']
			model = request.form['carmodel']
			regno = request.form['regno']
			location = request.form['location']
			con = mysql.connection
			cur = con.cursor()
			cur.execute("Use car_rental;")
			cur.execute("Insert into Car_Details values("+deposit+",'"+model+"','"+regno+"','"+location+"');")
			con.commit()
			return render_template('admin.html',flag = 0)
		elif request.form['submit'] == "Car Remove":
			regno = request.form['regno']
			con = mysql.connection
			cur = con.cursor()
			cur.execute("Use car_rental;")
			cur.execute("Delete from Car_Details where Registration_Number like '"+regno+"';")
			con.commit()
			return render_template('admin.html',flag = 0)
		elif request.form['submit'] == "Car Modify":
			regno = request.form['regno']
			field = request.form['field']
			value = request.form['value']
			con = mysql.connection
			cur = con.cursor()
			cur.execute("Use car_rental;")
			cur.execute("Update Car_Details set" + field + " = "+ value+"where Registration_Number like '"+regno+"';")
			cur.commit()
			return render_template('admin.html',flag = 0)
		elif request.form['submit'] == "Customer Remove":
			cid = request.form['C_ID']
			con = mysql.connection
			cur = con.cursor()
			cur.execute("Use car_rental;")
			cur.execute("Delete from Customer where C_ID = "+cid+";")
			con.commit()
			return render_template('admin.html',flag = 0)
		elif request.form['submit'] == "Customer Modify":
			cid = request.form['CID']
			field = request.form['field']
			value = request.form['value']
			con = mysql.connection
			cur = con.cursor()
			cur.execute("Use car_rental;")
			cur.execute("Update Customer set"+field+"="+value+"where C_ID is "+cid+";")
			con.commit()
			return render_template('admin.html',flag = 0)
		elif request.form['submit'] == "Chauffeur Add":		
			cid = request.form['Chauffeur_ID']
			name = request.form['Chauffeur_Name']
			dlno = request.form['DL_Number']
			phc = request.form['Per_Hour_Charges']
			location = request.form['location']
			con = mysql.connection
			cur = con.cursor()
			cur.execute("Use car_rental;")
			cur.execute("Insert into Chauffeur values("+cid+",'"+name+"','"+dlno+"',"+phc+",'"+location+"');")
			con.commit()
			return render_template('admin.html',flag = 0)
		elif request.form['submit'] == "Chauffuer Remove":
			cid = request.form['C_ID']
			con = mysql.connection
			cur = con.cursor()
			cur.execute("Use car_rental;")
			cur.execute("Delete from Chauffeur where Chauffuer_ID = "+cid+";")
			con.commit()
			return render_template('admin.html',flag = 0)
		elif request.form['submit'] == "Chauffeur Modify":
			cid = request.form['CID']
			field = request.form['field']
			value = request.form['value']
			con = mysql.connection
			cur = con.cursor()
			cur.execute("Use car_rental;")
			cur.execute("Update Chauffeur set"+field+"="+value+"where C_ID is "+cid+";")
			con.commit()
			return render_template('admin.html',flag = 0)
			
			

		
	else:
		return render_template('admin.html',flag = 0)

@app.route('/billconfirm',methods = ['GET','POST'])
def billconfirm():
	if request.method == 'POST':
			bill_id = request.form['search']
			con = mysql.connection
			cur = con.cursor()
			cur.execute("Use car_rental;")
			cur.execute("Select Bill_ID, Base_Amount,Booking_Date,Booking_Duration,Registration_Number,Chauffeur_ID,C_ID,Status from Billing where Bill_ID ="+bill_id+";")
			data = cur.fetchall()
			return render_template("billconfirm.html", flag = 1,item = data[0])
	else:
		return render_template("billconfirm.html", flag = 0)

@app.route('/billconfirm2/<int:ID>',methods = ['GET','POST'])
def billconfirm2(ID):
	if request.method == 'POST':
		ed = request.form['Extra_Distance']
		et = request.form['Extra_Time']
		cc = request.form['Chauffeur_Charges']
		oc = request.form['Other_Charges']
		con = mysql.connection
		cur = con.cursor()
		cur.execute("Use car_rental;")
		cur.execute("Update Billing set Extra_Distance="+ed+",Extra_Time="+et+", Chauffeur_Charges="+cc+" , Other_Charges="+oc+" where Bill_ID ="+ID+";")	
		con.commit()
		return redirect(url_for('admin',flag = 0))

if __name__ == '__main__':
   app.run(debug = True)
