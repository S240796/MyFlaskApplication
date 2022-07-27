from flask import Flask,render_template,request
import pymysql
MyFirstApp = Flask(__name__)

db = None
cur = None
def connectDB():
    global db,cur
    db = pymysql.connect(host='localhost',
                     user='shubham',
                     password='',
                     database='python_3_10_2')
    cur = db.cursor()
    
    
def disconnectDB():
    db.close()
    cur.close()

def readallrecords():
    connectDB()
    query = 'select * from employees'
    cur.execute(query)
    result = cur.fetchall()
    disconnectDB()
    return result

def searchrecord(ID):
    connectDB()
    query = f'select * from employees where EMPLOYEE_ID = {ID}'
    cur.execute(query)
    result = cur.fetchone()
    return result
    disconnectDB()

def deleterecord(ID):
    connectDB()
    #i = int(input('Enter EMPLOYEE_ID to serch data :'))
    query = f'delete from employees where EMPLOYEE_ID = {ID}'
    cur.execute(query)
    db.commit()    
    disconnectDB()
    
def insertrecord(EMPLOYEE_ID,FIRST_NAME,LAST_NAME,EMAIL,PHONE,HIRE_DATE,MANAGER_ID,JOB_TITLE):
    connectDB()
    query = f'Insert into EMPLOYEES(EMPLOYEE_ID,FIRST_NAME,LAST_NAME,EMAIL,PHONE,HIRE_DATE,MANAGER_ID,JOB_TITLE)values({EMPLOYEE_ID},"{FIRST_NAME}","{LAST_NAME}","{EMAIL}","{PHONE}",current_date(),{MANAGER_ID},"{JOB_TITLE}")'
    #print(query)
    cur.execute(query)
    db.commit()

def updatedata(EMPLOYEE_ID,FIRST_NAME,LAST_NAME,EMAIL,PHONE,HIRE_DATE,MANAGER_ID,JOB_TITLE):
    connectDB()
    query = f'update EMPLOYEES set FIRST_NAME="{FIRST_NAME}",LAST_NAME="{LAST_NAME}",EMAIL="{EMAIL}",PHONE="{PHONE}",HIRE_DATE="{HIRE_DATE}",MANAGER_ID={MANAGER_ID},JOB_TITLE="{JOB_TITLE}" where EMPLOYEE_ID={EMPLOYEE_ID}'
    cur.execute(query)
    db.commit()
    disconnectDB()  

@MyFirstApp.route('/')
def homepage():
    return render_template('Index.html',data = readallrecords())


@MyFirstApp.route('/update')
def gotoupdate():
    return render_template('update.html',data = readallrecords())


@MyFirstApp.route('/delete')
def gotodelete():
    return render_template('delete.html',data = readallrecords())

@MyFirstApp.route('/updatedata/<ID>',methods=['POST','GET'])
def update(ID):
    if request.method=='POST':
        #EMPLOYEE_ID = request.form['Employee_Id']
        FIRST_NAME  = request.form['First_Name']
        LAST_NAME   = request.form['Last_Name']
        EMAIL       = request.form['Email']
        PHONE       = request.form['Phone_No']
        HIRE_DATE   = request.form['Hire_Date']
        MANAGER_ID  = request.form['Manager_Id']
        JOB_TITLE   = request.form['Job_Tittle']
        updatedata(ID,FIRST_NAME,LAST_NAME,EMAIL,PHONE,HIRE_DATE,MANAGER_ID,JOB_TITLE)
        return render_template('Index.html',data = readallrecords())
    else:
        return render_template('updatedata.html',data = searchrecord(ID))

@MyFirstApp.route('/delete/<ID>')
def delete(ID):
    deleterecord(ID)
    #return 'Delete'
    return render_template('Index.html',data = readallrecords())

@MyFirstApp.route('/aboutus')
def aboutus():
    return 'HI'
@MyFirstApp.route('/insert')
def insert():
    EMPLOYEE_ID = request.args.get('Employee Id')
    FIRST_NAME  = request.args.get('First Name')
    LAST_NAME   = request.args.get('Last Name')
    EMAIL       = request.args.get('Email')
    PHONE       = request.args.get('Phone No')
    HIRE_DATE   = request.args.get('Hire Date')
    MANAGER_ID  = request.args.get('Manager Id')
    JOB_TITLE   = request.args.get('Job Tittle')
    if (EMPLOYEE_ID==None or FIRST_NAME==None or LAST_NAME==None or EMAIL==None or
        PHONE==None or HIRE_DATE==None or MANAGER_ID==None or JOB_TITLE==None):
        return render_template('insert.html')
    else:
        insertrecord(EMPLOYEE_ID,FIRST_NAME,LAST_NAME,EMAIL,PHONE,HIRE_DATE,MANAGER_ID,JOB_TITLE)
        return render_template('Index.html',data = readallrecords())

if __name__ == '__main__':
    MyFirstApp.run(debug=True)
