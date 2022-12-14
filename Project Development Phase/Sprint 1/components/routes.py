from components import app, conn, bcrypt,db2
from flask import render_template, flash, request, url_for, redirect,session
import ibm_db


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['user_password']

        query = "SELECT * FROM JBG49873.USER WHERE USER.USERNAME = ? LIMIT 1";
        prep_stmt = ibm_db.prepare(conn,query)
        ibm_db.bind_param(prep_stmt, 1, user_name)
        ibm_db.execute(prep_stmt)
        result_dict = ibm_db.fetch_assoc(prep_stmt)
        if result_dict and bcrypt.check_password_hash(result_dict['PASSWORD'], password):
            session['loggedin'] = True
            session['id'] = result_dict['USER_ID']
            session['username'] = result_dict['USERNAME']
            flash(f'Log into the account successfully!!',category='success')
            return redirect(url_for('dashboard_page'))
        else:
            flash(f'Username and/or password are incorrect to login!',
                  category='danger')
            return redirect(url_for('home_page'))

    return render_template('home.html')


@app.route("/", methods=['GET', 'POST'])
def register_page():
    error_msg = []
    msg = ''
    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        user_name = request.form['uname']
        email_id = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # check username exist
        query = "SELECT COUNT(USERNAME) AS IS_PRESENT FROM JBG49873.USER WHERE USER.USERNAME = ?;"
        prep_stmt = ibm_db.prepare(conn, query)
        ibm_db.bind_param(prep_stmt, 1, user_name)
        ibm_db.execute(prep_stmt)
        result_dict = ibm_db.fetch_assoc(prep_stmt)
        if result_dict['IS_PRESENT'] >= 1:
            error_msg.append("username already exist. try other username!")

        # check emailid exist
        query = "SELECT COUNT(USERNAME) AS IS_PRESENT FROM JBG49873.USER WHERE USER.EMAIL_ID = ?;"
        prep_stmt = ibm_db.prepare(conn, query)
        ibm_db.bind_param(prep_stmt, 1, email_id)
        ibm_db.execute(prep_stmt)
        result_dict = ibm_db.fetch_assoc(prep_stmt)
        if result_dict['IS_PRESENT'] >= 1:
            error_msg.append("email id already exist.try other emailid!")

        # check password and confirm password are equal
        if password != confirm_password:
            error_msg.append("password and confirm password are not same")

        if len(error_msg) > 0:
            for i in error_msg:
                flash(f'There was an error with creating a user: {i}',
                      category='danger')
            return redirect(url_for('home_page'))

        else:
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

            query = "INSERT INTO JBG49873.USER(" \
                    "FIRST_NAME,LAST_NAME,USERNAME,EMAIL_ID,PASSWORD" \
                    ") VALUES (?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, query)
            ibm_db.bind_param(prep_stmt, 1, first_name)
            ibm_db.bind_param(prep_stmt, 2, last_name)
            ibm_db.bind_param(prep_stmt, 3, user_name)
            ibm_db.bind_param(prep_stmt, 4, email_id)
            ibm_db.bind_param(prep_stmt, 5, password_hash)
            ibm_db.execute(prep_stmt)
            flash(f'Account created successfully!!',
                  category='success')
            return redirect(url_for('login_page'))


@app.route('/dashboard')
def dashboard_page():
    if 'id' in session:
        return render_template('dashboard.html')
    else:
        flash(f'Cant see this page without login!!',
              category='danger')
        return redirect(url_for('home_page'))

@app.route('/inventory')
def inventory_page():
    if 'id' in session:
        return render_template('inventory.html')
    else:
        flash(f'Cant see this page without login!!',
              category='danger')
        return redirect(url_for('home_page'))


@app.route('/logs')
def logs_page():
    if 'id' in session:
        return render_template('logs.html')
    else:
        flash(f'Cant see this page without login!!',
              category='danger')
        return redirect(url_for('home_page'))



@app.route('/track')
def track_page():
    if 'id' in session:
        return render_template('track.html')
    else:
        flash(f'Cant see this page without login!!',
              category='danger')
        return redirect(url_for('home_page'))


@app.route('/logout')
def logout_page():
    if 'id' in session:
            session.pop('id',None)
            session.pop('username',None)
            flash("You have been logged out!", category='success')
            return redirect(url_for('home_page'))
    else:
        flash(f'You are already logged out',
              category='danger')
        return redirect(url_for('home_page'))