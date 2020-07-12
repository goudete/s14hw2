from flask import Flask, render_template, request, redirect, url_for
from models.user import db, User
from modules.userform import UserForm
from modules.edituserform import EditUserForm
from modules.mockdata import MockDataForm
import os


import random
import string


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "s14a-key"
db.init_app(app)

@app.route('/')
def index():
    users = User.query.all()
    mockdataform = MockDataForm()
    for user in users:
        User.toString(user)

    return render_template("index.html", users=users, mockdataform=mockdataform)

# @route /adduser - GET, POST
@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    form = UserForm()
    # If GET
    if request.method == 'GET':
        return render_template('adduser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            first_name = request.form['first_name']
            age = request.form['age']
            new_user = User(first_name=first_name, age=age)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('adduser.html', form=form)


# @route /adduser/<first_name>/<age>
@app.route('/adduser/<first_name>/<age>')
def addUserFromUrl(first_name, age):
    db.session.add(User(first_name=first_name, age=age))
    db.session.commit()
    return redirect(url_for('index'))


#Read route for individual user
@app.route('/aboutuser/<user_id>')
def aboutuser(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    return render_template('about_user.html', user=user)

@app.route('/deleteuser/<user_id>')
def deleteuser(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/updateuser/<user_id>', methods=('GET', 'POST'))
def updateuser(user_id):
    edit_form = EditUserForm()
    user = User.query.filter_by(user_id=user_id).first()

    if request.method == 'GET':
        return render_template('edit_user.html', edit_form=edit_form, user=user)
    else:
        if edit_form.validate_on_submit():
            edit_first_name = request.form['edit_first_name']
            edit_age = request.form['edit_age']

            user.first_name = edit_first_name
            user.age = edit_age
            db.session.commit()
            return redirect(url_for('index'))

        else:
            return render_template('edit_user.html', edit_form=edit_form)

#helper function to generate random string
def generate_name():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(7))
    return result_str

def generate_age():
    age = random.randint(0, 100)
    return age

@app.route('/mockdata', methods=('GET', 'POST'))
def mockdata():
    if request.method == 'POST':
        number = int(request.form['number-mock'])
        #generate mock data
        instances = []
        for i in range(number):
            first_name = generate_name()
            age = generate_age()
            instances.append(User(first_name=first_name, age=age))

        #insert into db
        db.session.add_all(instances)
        db.session.commit()

        return redirect(url_for('index'))
