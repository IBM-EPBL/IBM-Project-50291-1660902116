##  DB2 and Flask connection


```ruby
from flask import Flask, render_template
import ibm_db
from flask_bcrypt import Bcrypt
from sqlalchemy import *
from flask_sqlalchemy import  SQLAlchemy
import ibm_db_sa
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '01845a0438c36160cbe978ea'
app.config['SQLALCHEMY_DATABASE_URI'] = 'db2+ibm_db://jbg49873:CWnz9f65Zdaixqgw@b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud:31249/bludb'

try:
    db2 = SQLAlchemy(app)
    conn = ibm_db.connect(
        'DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;PROTOCOL=TCPIP;UID=jbg49873;PWD=CWnz9f65Zdaixqgw;Security=SSL;SSLSecurityCertificate=DigiCertGlobalRootCA.crt',
        '', '')
except:
    print("[+]\tConnecting to DB2 [FAIL] : ", ibm_db.conn_errormsg())
else:
    print("[+]\tConnecting to DB2 [SUCCESS]")
bcrypt = Bcrypt(app)

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
        
```

### OUTPUT

![image](https://user-images.githubusercontent.com/64410018/202899246-8f35de57-d7a7-47b9-845c-a969954742c9.png)

![image](https://user-images.githubusercontent.com/64410018/202899288-913f0600-25b2-4e03-b7c8-1d98bebe1baf.png)

![image](https://user-images.githubusercontent.com/64410018/202899301-f2f8ac73-2121-41fd-a9c6-b1945c6bf15e.png)

![image](https://user-images.githubusercontent.com/64410018/202899344-17b973c1-e396-49ee-b31c-0a90833070a2.png)


