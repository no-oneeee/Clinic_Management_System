from flask import Flask, render_template, request, redirect, url_for, session,render_template_string
from queries_database import ClinicData

app = Flask(__name__)
app.secret_key = 'your_secret_key'
my_clinic = ClinicData('ads','password','localhost')

@app.route('/', methods=['GET'])
def redirected():
    return redirect(url_for('patient_login'))

@app.route('/patient_login',methods=['POST','GET'])
def patient_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if password != my_clinic.get_patient_password(username):
            error = "username or password does not match"
            return render_template('login.html',error=error)
        else:
            session['username'] = username
            return redirect(url_for('my_home'))
    return render_template('login.html')

@app.route('/patient_register',methods=["POST","GET"])
def patient_register():
    if request.method == 'POST':
        username = request.form['username']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        gender = request.form['gender']
        if gender == '0':
            sex = 'MALE'
        elif gender == '1':
            sex = 'FEMALE'
        else:
            sex = "OTHER"
        password = request.form['password']
        c = my_clinic.set_patient_data(username,password,fname,lname,phone,sex)
        if c == True:
            print('Success')
        else:
            error = "Username already taken"
            print(c)
            return render_template('signup.html',error=error)
        return redirect(url_for('patient_login'))
    return render_template('signup.html')

@app.route('/doctor_login',methods=['POST','GET'])
def doctor_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if password != my_clinic.get_doctor_password(username):
            error = "username or password does not match"
            return render_template('doctorlogin.html',error=error)
        else:
            session['username'] = username
            return redirect(url_for('my_dochome'))
    return render_template('doctorlogin.html')

@app.route('/doctor_register',methods=['POST','GET'])
def doctor_register():
    if request.method == 'POST':
        username = request.form['username']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        gender = request.form['gender']
        if gender == '0':
            sex = 'MALE'
        elif gender == '1':
            sex = 'FEMALE'
        else:
            sex = "OTHER"
        password = request.form['password']
        c = my_clinic.set_doctor_data(username,password,fname,lname,phone,sex)
        if c == True:
            print('Success')
        else:
            error = "Username already taken"
            print(c)
            return render_template('doctorsignup.html',error=error)
        return redirect(url_for('doctor_login'))
    return render_template('doctorsignup.html')

@app.route('/home')
def my_home():
    return render_template('home.html',username=session['username'])

@app.route('/doctorhome')
def my_dochome():
    return render_template('doctorhome.html',username=session['username'])

@app.route('/schedule_shift',methods=['POST','GET'])
def schedule_shift():
    if request.method == 'POST':
        dname = session['username']
        shift = request.form['start_loc']
        date = request.form['date']
        c = my_clinic.schedule_shift(dname,shift,date)
        if c == True:
            message = "Shift scheduled"
            return render_template('docshifts.html',message=message)
        else:
            error = "Shift not scheduled"
            return render_template('docshifts.html',error=error)
        return render_template('docshifts.html')
    return render_template('docshifts.html')

@app.route('/delete_app',methods=['POST','GET'])
def delete_app():
    if request.method == 'POST':
        pname = request.form['start_loc']
        shift = request.form['sft']
        date = request.form['date']
        c = my_clinic.delete_app(pname,shift,date)
        if c == True:
            message = "Appointment deleted"
            return render_template('examined.html',message=message)
        else:
            error = "Patient not found"
            return render_template('examined.html',error=error)
        return render_template('examined.html')
    return render_template('examined.html')

@app.route('/schedule_app',methods=['POST','GET'])
def schedule_app():
    if request.method == 'POST':
        uname = session['username']
        pname = request.form['name']
        dname = request.form['docname']
        shift = request.form['start_loc']
        date = request.form['date']
        c = my_clinic.schedule_app(uname,pname,dname,shift,date)
        if c == True:
            message = "Booking successful"
            return render_template('appointment.html',message=message)
        else:
            error = "Doctor not available"
            return render_template('appointment.html',error=error)
        return render_template('appointment.html')
    return render_template('appointment.html')

@app.route('/order_meds',methods=['POST','GET'])
def order_meds():
    if request.method == 'POST':
        mname = request.form['start_loc']
        supply = request.form['number']
        sup = request.form['number']
        c = my_clinic.order_meds(supply,mname,sup)
        print(c)
        if c == True:
            message = "Order successful"
            return render_template('pharmacy.html',message=message)
        else:
            error = "Medicine not available"
            return render_template('pharmacy.html',error=error)
        return render_template('pharmacy.html')
    return render_template('pharmacy.html')

@app.route('/add_meds',methods=['POST','GET'])
def add_meds():
    if request.method == 'POST':
        mname = request.form['start_loc']
        supply = request.form['number']
        c = my_clinic.add_meds(supply,mname)
        if c == True:
            message = "Add successful"
            return render_template('addmeds.html',message=message)
        else:
            error = "Add unsuccessful"
            return render_template('addmeds.html',error=error)
        return render_template('addmeds.html')
    return render_template('addmeds.html')

@app.route('/check_meds',methods=['POST','GET'])
def check_meds():
    if request.method == 'POST':
        mname = request.form['start_loc']
        c = my_clinic.check_meds(mname)
        if c == False:
            error = "Medicine not found"
            return render_template('docpharmacy.html',error=error)
        else:
            message = str(c)
            return render_template('docpharmacy.html',message=message)
        return render_template('docpharmacy.html')
    return render_template('docpharmacy.html')

@app.route('/check_shifts',methods=['POST','GET'])
def check_shifts():
    if request.method == 'POST':
        shift = request.form['start_loc']
        date = request.form['date']
        c = my_clinic.check_shifts(shift,date)
        if c == False:
            error = "Doctors not available"
            return render_template('shifts.html',error=error)
        else:
            message = str(c)
            return render_template('shifts.html',message=message)
        return render_template('shifts.html')
    return render_template('shifts.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('patient_login'))

@app.route('/doctor_logout')
def doctor_logout():
    session.pop('username', None)
    return redirect(url_for('doctor_login')) 

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=8888)
