

### app.py

```ruby
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

```

### /template/register.html

```ruby
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>login</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    </head>
    <body>
        <form action="{{ url_for('register') }}" method="post">
            <div class="container">
                <h2 class="reg">Create your own account!</h2>
                <input type="text" placeholder="Enter Username" name="username" required>
                <input type="text" placeholder="Enter rollno" name="rollno" required>
                <input type="text" placeholder="Enter email" name="emailid" required>
                <input type="password" placeholder="Enter Password" name="password" required>
                <button type="submit">Login</button>
                <label>
                  <input type="checkbox" checked="checked" name="remember"> Remember me
                </label>
              </div>
            
              <div class="container" style="background-color:#f1f1f1">
                <button type="button" class="cancelbtn">Cancel</button>
                <span class="psw"><a href="{{url_for('login')}}">Already have an account?</a></span>
              </div>
        </form>
    </body>
</html>
```

### /template/login.html

```ruby
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>login</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" />
    </head>
    <body>
        <form action="{{ url_for('login') }}" method="post">
            <div class="imgcontainer">
                <img src="{{ url_for('static', filename='img_avatar2.png') }}" alt="Avatar" class="avatar">
            </div>
            <div class="container">
                <label for="username"><b>Username</b></label>
                <input type="text" placeholder="Enter Username" name="username" required>
            
                <label for="password"><b>Password</b></label>
                <input type="password" placeholder="Enter Password" name="password" required>
                    
                <button type="submit">Login</button>
                <label>
                  <input type="checkbox" checked="checked" name="remember"> Remember me
                </label>
              </div>
            
              <div class="container" style="background-color:#f1f1f1">
                <button type="button" class="cancelbtn">cancel</button>
                <span class="psw"><a href="{{url_for('register')}}">Didnt have an account?</a></span>
              </div>
            </form>
    </body>
</html>

```

### /template/login.html

```ruby
<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>login</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" />
</head>

<body>
    <div class="imgcontainer">
        <img src="{{ url_for('static', filename='img_avatar2.png') }}" alt="Avatar" class="avatar">
    </div>
    <div class="container">
        <h2 class="reg">Welcome home!</h2>
    </div>
</body>

</html>
```

## OUTPUT

![image](https://user-images.githubusercontent.com/64410018/202899590-0b9622a3-14ea-4bcb-83d9-bf39ca6a0528.png)

![image](https://user-images.githubusercontent.com/64410018/202899603-7caa674a-1e0c-4bd4-8d20-c36ba5ca62a3.png)

![image](https://user-images.githubusercontent.com/64410018/202899614-a296ce10-4b25-4541-88ed-43cdf37e1151.png)
