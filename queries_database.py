import mysql.connector

class ClinicData:
    def __init__(self, username, password, host_name):
        self.dataBase = mysql.connector.connect(
            host = host_name,
            user = username,
            passwd = password,
            allow_local_infile = True,
            auth_plugin = 'mysql_native_password',
            database = 'clinic'
        )
        self.cursorObject = self.dataBase.cursor()
        print('DataBase Initialised successfully')

    def set_patient_data(self, username, password, first_name, last_name, phone_number, gender):
        query = """insert into LoginPatient values (%s, %s, %s, %s, %s, %s)"""
        parameters = (username,first_name,last_name,phone_number,gender,password)
        try:
            self.cursorObject.execute(query, parameters)
        except mysql.connector.Error as err:
            return err
        self.dataBase.commit()
        return True
    
    def set_doctor_data(self, username, password, first_name, last_name, phone_number, gender):
        query = """insert into LoginDoctor values (%s, %s, %s, %s, %s, %s)"""
        parameters = (username,first_name,last_name,phone_number,gender,password)
        try:
            self.cursorObject.execute(query, parameters)
        except mysql.connector.Error as err:
            return err
        self.dataBase.commit()
        return True

    def get_patient_password(self,username):
        query = "select Password from LoginPatient where username = %s"
        parameters = (username,)
        self.cursorObject.execute(query, parameters)
        data = self.cursorObject.fetchall()
        if len(data) > 0:
            return (data[0])[0]
        else:
            return False
    
    def get_doctor_password(self,username):
        query = "select Password from LoginDoctor where username = %s"
        parameters = (username,)
        self.cursorObject.execute(query, parameters)
        data = self.cursorObject.fetchall()
        if len(data) > 0:
            return (data[0])[0]
        else:
            return False

    def get_patient_data(self, username):
        query = """select P_Name, DOC_Name, shift, my_day from Appointments where username = %s"""
        parameters = (username, )
        self.cursorObject.execute(query, parameters)
        data = self.cursorObject.fetchall()
        if len(data) > 0:
            return (data[0])
        else:
            return False

    def get_doctor_data(self, username):
        query = """select P_Name, shift, my_day from Appointments where username = %s"""
        parameters = (username, )
        self.cursorObject.execute(query, parameters)
        data = self.cursorObject.fetchall()
        if len(data) > 0:
            return (data[0])
        else:
            return False

    def schedule_shift(self, dname, shift, date):
        query = """insert into Doctor values (%s, %s, %s)"""
        parameters = (dname,shift,date)
        try:
            self.cursorObject.execute(query, parameters)
        except mysql.connector.Error as err:
            print(err)
            return(err)
        self.dataBase.commit()
        return True

    def delete_app(self, pname, shift, date):
        query = """select * from Appointments where P_Name=%s and shift=%s and my_day=%s
        """
        parameters = (pname,shift,date)
        try:
            self.cursorObject.execute(query,parameters)
            data = self.cursorObject.fetchall()
            if len(data)>0:
                query = """delete from Appointments where P_Name=%s and shift=%s and my_day=%s"""
                parameters = (pname,shift,date)
                try:
                    self.cursorObject.execute(query, parameters)
                except mysql.connector.Error as err:
                    print(err)
                    return(err)
                self.dataBase.commit()
                return True
            else:
                return False
        except:
            return False

    def schedule_app(self, uname, pname, dname, shift, date):
        query = """select * from Doctor where shift=%s and my_day=%s"""
        parameters = (shift, date)
        self.cursorObject.execute(query, parameters)
        data = self.cursorObject.fetchall()
        if len(data) > 0:
            query = """insert into Appointments values (%s, %s, %s, %s, %s)"""
            parameters = (uname, pname, dname, shift, date)
            try:
                self.cursorObject.execute(query, parameters)
            except mysql.connector.Error as err:
                print(err)
                return(err)
            self.dataBase.commit()
            return True
        else:
            return False
        
    def order_meds(self, supply, mname, sup):
        query = """select * from Pharmacy where MED_Name = %s and Supply>%s
        """
        parameters = (mname,sup)
        try:
            self.cursorObject.execute(query,parameters)
            data = self.cursorObject.fetchall()
            if len(data)>0:
                query = """update Pharmacy set Supply=Supply - %s where MED_Name=%s and Supply>%s"""
                parameters = (supply,mname,sup)
                try:
                    self.cursorObject.execute(query, parameters)
                except mysql.connector.Error as err:
                    print(err)
                    return(err)
                self.dataBase.commit()
                return True
            else:
                return False
        except:
            return False

    def add_meds(self, supply, mname):
        query = """select * from Pharmacy where MED_Name = %s
        """
        parameters = (mname,)
        try:
            self.cursorObject.execute(query,parameters)
            data = self.cursorObject.fetchall()
            if len(data)>0:
                query = """update Pharmacy set Supply=Supply + %s where MED_Name=%s"""
                parameters = (supply,mname)
                try:
                    self.cursorObject.execute(query, parameters)
                except mysql.connector.Error as err:
                    print(err)
                    return(err)
                self.dataBase.commit()
                return True
            else:
                return False
        except:
            return False

    def check_meds(self, mname):
        query = """select Supply from Pharmacy where MED_Name=%s"""
        parameters = (mname,)
        self.cursorObject.execute(query, parameters)
        data = self.cursorObject.fetchall()
        if len(data) > 0:
            return (data[0])[0]
        else:
            return False

    def check_shifts(self, shift, date):
        query = """select DOC_Name from Doctor where shift=%s and my_day=%s"""
        parameters = (shift,date)
        self.cursorObject.execute(query, parameters)
        data = self.cursorObject.fetchall()
        if len(data) > 0:
            return (data[0])[0]
        else:
            return False