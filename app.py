from flask import Flask,render_template,redirect,url_for,request
import pymysql




#create the object of the class Flask
app=Flask(__name__)  


#A method that will invoke  server execution 
@app.route('/')                                              #annotation/decorator
def index():
    #return 'Hello Boss ....I am Working'
    return render_template('index.html')

@app.route("/sign_up", methods=['GET']) 
def signup():
    return render_template('signup.html')

@app.route("/log_in", methods=['GET']) 
def login():
    return render_template('login.html')

@app.route("/consult", methods=['GET']) 
def consult():
    return render_template('consult.html')


def insert_values(nm,eid,pw,ph,add):
      con = pymysql.connect(user="root", password="", host="localhost", database="hospitalserver")
      cur = con.cursor()
      insert_query = "INSERT INTO admin (admin_nm, admin_email,admin_pw,admin_ph,admin_add) VALUES (%s, %s, %s,%s,%s);"
      cur.execute(insert_query, (nm,eid,pw,ph,add))
      con.commit()
      cur.close()
      con.close()


def insert_values1(nm,sp,eid,pw,ph,add):
      con = pymysql.connect(user="root", password="", host="localhost", database="hospitalserver")
      cur = con.cursor()
      insert_query = "INSERT INTO doctor (doc_nm,speciality, doc_email,doc_pw,doc_ph,doc_add) VALUES (%s, %s, %s,%s,%s,%s);"
      cur.execute(insert_query, (nm,sp,eid,pw,ph,add))
      con.commit()
      cur.close()
      con.close()



@app.route("/register", methods=['POST','GET']) 
def register():
    if request.method =='POST':
        try:

           data=request.form
           User_mode=data['User_type']
           if User_mode=='admin':
               insert_values(data['u_nm'],data['e_id'],data['u_pw'],data['ph_num'],data['add'])
               msg='Record added successfully'

           else:
              #insert_values1(data['u_nm'],data['sp'],data['e_id'],data['u_pw'],data['ph_num'],data['add'])
              pass

             # msg='Record added successfully'

        except:
            msg='Record Unsuccessfully added'
        finally: 
             
            return redirect(url_for('success',smg=msg)) 
            


@app.route("/register1", methods=['POST','GET']) 
def register1():
    if request.method =='POST':
        data=request.form
        insert_values1(data['u_nm'],data['u_sp'],data['e_id'],data['u_pw'],data['ph_num'],data['add'])
        msg='Record added successfully'
        return redirect(url_for('success',smg=msg))




@app.route('/success/<smg>')
def success(smg):
    return 'welcome %s' % smg



def insert_consult(nm,age,eid,ph,type,add):
      con = pymysql.connect(user="root", password="", host="localhost", database="hospitalserver")
      cur = con.cursor()
      insert_query = "INSERT INTO patient (p_nm, p_age,p_eid,p_ph,speciality,p_add) VALUES (%s, %s, %s,%s,%s,%s);"
      cur.execute(insert_query, (nm,age,eid,ph,type,add))
      con.commit()
      cur.close()
      con.close()


#Code build to book an appointment .... 

@app.route("/consult", methods=['POST'])                                   #consult Post method
def consult1():
    if request.method =='POST': 
        data=request.form 
        insert_consult(data['u_nm'], data['age'], data['e_id'],data['ph_num'],data['User_type'],data['add']) 
        #msg=data['User_type'].upper()
        msg=(data['User_type'].upper() +'.....'+'can be consulted between 6 -9 PM')
        return render_template('history.html',data=msg)


def insert_history(nm,age,ph,pr,mor):
      con = pymysql.connect(user="root", password="", host="localhost", database="hospitalserver")
      cur = con.cursor()
      insert_query = "INSERT INTO pat_history (p_nm, p_age,p_ph,report,comorbid) VALUES (%s, %s, %s,%s,%s);"
      cur.execute(insert_query, (nm,age,ph,pr,mor))
      con.commit()
      cur.close()
      con.close()        


@app.route("/history", methods=['POST'])                                    #history Post method
def history():
    if request.method =='POST': 
        data=request.form 
        insert_history(data['u_nm'], data['age'],data['ph_num'],data['pro'],data['co_mor']) 
        msg = 'Sucessfully Completed Your Slot is Confirmed.....!!'
        return (msg)


def load_history_view():
    con = pymysql.connect(user="root", password="", host="localhost", database="hospitalserver")
    cur = con.cursor()
    cur.execute("SELECT * FROM pat_history")
    data = cur.fetchall()                                                     #we shall get result as tuple of tuples
    cur.close()
    con.close()
    return data


@app.route("/historyview", methods=['GET'])                                  #to view patient history table
def historyview():
    data= load_history_view()
    return render_template('doctor.html',data2=data)
        
       





#log In verification code::: Begin

@app.route("/signinverify", methods=['POST','GET'])
def signinverify():
     con = pymysql.connect(user="root", password="", host="localhost", database="hospitalserver")
     cur = con.cursor()
     if request.method =='POST': 
        data=request.form 
        if data['User_type']=='admin':
            email=data['e_id']
            pw=data['u_pw']
            #cur.execute("select * from admin where admin_email='"+email+"' and admin_pw='"+pw+"'")
            cur.execute("select * from admin where admin_email=%s and admin_pw=%s",(email,pw))
            r=cur.fetchall()
            count=cur.rowcount
            if count==1:
                return render_template('admin.html')
            else:
                return render_template('login.html')

            
        else:
            email=data['e_id']
            pw=data['u_pw']
           # cur.execute("select * from doctor where doc_email='"+email+"' and doc_pw='"+pw+"'")
            cur.execute("select * from doctor where doc_email= %s and doc_pw=%s",(email,pw))
            r=cur.fetchall()
            count=cur.rowcount                                       #syntax :: cur_object.rowcount 
            if count==1:
                return render_template('doctor.html')
            else:
                return render_template('login.html')
        

 #log in verification code :: End 


def load():
    con = pymysql.connect(user="root", password="", host="localhost", database="hospitalserver")
    cur = con.cursor()
    cur.execute("SELECT * FROM doctor")
    data = cur.fetchall()                                               #we shall get result as tuple of tuples
    cur.close()
    con.close()
    return data 



@app.route("/doc_on_duty", methods=['GET']) 
def duty():
    data= load()
    return render_template('admin.html',data=data)
    

def load1():
    con = pymysql.connect(user="root", password="", host="localhost", database="hospitalserver")
    cur = con.cursor()
    cur.execute("SELECT * FROM patient")
    data = cur.fetchall()                                                 #we shall get result as tuple of tuples
    cur.close()
    con.close()
    return data




@app.route("/patient_record", methods=['GET']) 
def patient():
    data= load1()
    return render_template('admin.html',data1=data)


@app.route("/patient_record1", methods=['GET'])                                 #to view in doctor html and allowing him to discharge
def patient1():
    data= load1()
    return render_template('doctor.html',data1=data)




@app.route("/appoint", methods=['GET']) 
def appoint():
    return render_template('drform.html')


def delete_doc(doc_id):
    con = pymysql.connect(user="root", password="", host="localhost", database="hospitalserver")
    cur = con.cursor()
    cur.execute("DELETE FROM doctor WHERE doc_id=%s;", (doc_id,))
    con.commit()
    cur.close()
    con.close()


@app.route("/relieve")
def relieve_doc():
    # From Url get ID
    doc_id = request.args.get('id', type=int)
    delete_doc(doc_id)
    return redirect(url_for("duty"))


def discharge_pat(dis_id):
    con = pymysql.connect(user="root", password="", host="localhost", database="hospitalserver")
    cur = con.cursor()
    cur.execute("update patient set status='Can be Discharged' WHERE p_id=%s;", (dis_id,))
    con.commit()
    cur.close()
    con.close()


@app.route("/discharge")
def discharge():
    # From Url get ID
    dis_id = request.args.get('id', type=int)
    discharge_pat(dis_id)
    return render_template('doctor.html')


def send_pat(sen_id):
    con = pymysql.connect(user="root", password="", host="localhost", database="hospitalserver")
    cur = con.cursor()
    cur.execute("DELETE FROM patient WHERE p_id=%s;", (sen_id,))
    con.commit()
    cur.close()
    con.close()


@app.route("/sendhome")
def sendhome():
    # From Url get ID
    sen_id = request.args.get('id', type=int)
    send_pat(sen_id)
    return render_template('admin.html')


def del_pat(del_id):
    con = pymysql.connect(user="root", password="", host="localhost", database="hospitalserver")
    cur = con.cursor()
    cur.execute("DELETE FROM pat_history WHERE h_id=%s;", (del_id))
    con.commit()
    cur.close()
    con.close()   


@app.route("/delhistory")
def delhistory():
    # From Url get ID
    del_id = request.args.get('id', type=int)
    del_pat(del_id)
    return render_template('doctor.html')






        





 





#To execute  this code we have to write
if __name__== '__main__' :
    app.run(debug=True)                                     #run is method of Flask

           