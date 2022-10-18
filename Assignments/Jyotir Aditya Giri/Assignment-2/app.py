from flask import Flask,render_template,request
import ibm_db

app = Flask(__name__)

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;PROTOCOL=TCPIP;UID=jbg49873;PWD=5K5X5cqNpuoBX0hI;Security=SSL;SSLSecurityCertificate=DigiCertGlobalRootCA.crt", "", "")
print("[+]\tConnected to DB2!")

@app.route("/",methods=['GET','POST'])
@app.route("/register",methods=['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form["username"]
        emailid = request.form["emailid"]
        password = request.form["password"]
        rollno = request.form["rollno"]
        
        sql = "INSERT INTO JBG49873.USER VALUES (?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(prep_stmt,1,username)
        ibm_db.bind_param(prep_stmt,2,emailid)
        ibm_db.bind_param(prep_stmt,3,password)
        ibm_db.bind_param(prep_stmt,4,rollno)
        ibm_db.execute(prep_stmt)
        return render_template('login.html',msg=msg)
    else:
        return render_template('register.html',msg=msg)


@app.route("/login",methods=['GET','POST'])
def login():
    msg=''
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT * FROM JBG49873.USER WHERE USERNAME = ? AND PASSWORD = ?"
        prep_stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(prep_stmt,1,username)
        ibm_db.bind_param(prep_stmt,2,password)
        out = ibm_db.execute(prep_stmt)
        result_dict = ibm_db.fetch_assoc(prep_stmt)
        print(result_dict)
        if result_dict != False:
            return render_template('welcome.html',msg = msg)
        return render_template('login.html', msg = msg)

    else:
        return render_template('login.html', msg = msg)

@app.route("/welcome",methods=['GET','POST'])
def welcome():
    msg = ''
    return render_template('welcome.html', msg = msg)

if __name__ == "__main__":
    app.run()
