from flask import Flask, redirect, url_for, request


class Signin:
    def __init__(self, name, email, password, address, gender, district):
        self.name = name
        self.email = email
        self.password = password
        self.gender = gender
        self.address = address
        self.city = district


app = Flask(__name__)
list = []


@app.route('/success/<name>')
def success(name):
    return 'welcome %s ' % name


@app.route('/success_update/<name>')
def success_update(name):
    return 'Updated Password successfully for user : %s ' % name


@app.route('/fail/<name>')
def fail(name):
    return 'Not founded : %s' % name


@app.route('/signin', methods=['POST', 'GET', 'PUT', 'DELETE'])
def signin():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['pwd']
        gender = request.form['gender']
        address = request.form['address']
        city = request.form['District']

        obj = Signin(name=name, email=email, password=pwd,
                     gender=gender, address=address, district=city)
        list.append(obj)

        return redirect(url_for('success', name=name))

    elif request.method == 'GET':
        name = request.form['name']
        pwd = request.form['pwd']
        flag = False

        for obj in list:
            if (obj.name == name and obj.password == pwd):
                flag = True
                return redirect(url_for('success', name=name))

        if (flag == False):
            return redirect(url_for('fail', name=name))

    elif request.method == 'PUT':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['pwd']
        flag = False

        for obj in list:
            if (obj.email == email and obj.name == name):
                obj.password = pwd
                flag = True
                return redirect(url_for('success_update', name=name))

    else:
        name = request.form['name']
        pwd = request.form['pwd']
        flag = False

        for obj in list:
            if (obj.name == name and obj.password == pwd):
                flag = True
                list.remove(obj)
                return "Deleted successfully"

        if (flag == False):
            return redirect(url_for('fail', name=name))


if __name__ == "__main__":
    app.run()