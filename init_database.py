import mysql.connector


dataBase = mysql.connector.connect(
    host="localhost",
    user="ads",
    passwd="password",
    allow_local_infile = True,
    auth_plugin='mysql_native_password'
)

cursorObject = dataBase.cursor()

createDoctor = "create table Doctor(DOC_Name varchar(30), shift varchar(10), my_day date, constraint scheck check(shift in ('Morning', 'Afternoon', 'Evening')), constraint pk primary key(DOC_Name,shift,my_day));"
createPatient = "create table Patient(P_Name varchar(30), DOC_Name varchar(30), GENDER varchar(10), constraint fk foreign key(DOC_Name) references Doctor(DOC_Name), constraint gcheck check(GENDER in ('Male', 'Female', 'Other')));"
createPharmacy = "create table Pharmacy(MED_Name varchar(30) primary key, Supply numeric(10));"
createAppointments = "create table Appointments(username varchar(20) references LoginPatient(username), P_Name varchar(30) references Patient(P_Name), DOC_Name varchar(30) references Doctor(DOC_Name), shift varchar(10), my_day date, constraint scheck1 check(shift in ('Morning', 'Afternoon', 'Evening')), constraint pk1 primary key(P_Name,shift,my_day));"
createLoginPatient = "create table LoginPatient(username varchar(20) primary key, F_Name varchar(30),L_Name varchar(30),Phone_Number numeric(10), GENDER varchar(10), Password varchar(30), constraint gcheck1 check(GENDER in ('Male', 'Female', 'Other')));"
createLoginDoctor = "create table LoginDoctor(username varchar(20) primary key, F_Name varchar(30),L_Name varchar(30),Phone_Number numeric(10), GENDER varchar(10), Password varchar(30), constraint gcheck2 check(GENDER in ('Male', 'Female', 'Other')));"

insertPharmacy = "insert into Pharmacy (MED_Name, Supply) values (%s, %s);"
parameters = [('Paracetamol',20),
        ('Aspirin',10),
        ('Benadryl',50),
        ('Meftalspas',30)]

cursorObject.execute("create database clinic")
cursorObject.execute("use clinic")
cursorObject.execute(createDoctor)
cursorObject.execute(createPatient)
cursorObject.execute(createPharmacy)
cursorObject.execute(createAppointments)
cursorObject.execute(createLoginPatient)
cursorObject.execute(createLoginDoctor)
cursorObject.executemany(insertPharmacy, parameters)
dataBase.commit()

# create table Pharmacy(MED_ID int primary key, Name varchar(30),Supply int, Salts varchar(50));

# create table Appointments(REF_ID int primary key, P_ID int, Time number(5,3),Date date, constraint fk4 foreign key(P_ID) references Patient(P_ID) on delete cascade);

# create table Prescription(PRE_ID int primary key, P_ID int, DOC_ID int, MED_ID int, Quantity int, constraint fk1 foreign key(P_ID) references Patient(P_ID) on delete cascade, constraint fk2 foreign key(DOC_ID) references Doctor(DOC_ID) on delete cascade, constraint fk3 foreign key(MED_ID) references Pharmacy(MED_ID) on delete cascade);

# create table Login(User_ID int primary key, F_Name varchar(30),L_Name varchar(30),Phone_Number int, GENDER varchar(10), Password varchar(30), constraint fk5 foreign key(User_ID) references Patient(P_ID) on delete cascade);
