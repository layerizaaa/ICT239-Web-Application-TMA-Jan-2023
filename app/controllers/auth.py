from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, redirect, render_template, url_for, flash
# from forms import RegForm
from models.forms import RegForm
from models.users import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.getUser(email=form.email.data)
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                User.createUser(email=form.email.data,password=hashpass, name=form.name.data)
                return redirect(url_for('auth.login'))
            else:
                form.email.errors.append("User is already registered.")
                render_template('register.html', form=form, panel="Register")    
            
    return render_template('register.html', form=form, panel="Register")

@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/')
def login():
    # if current_user.is_authenticated == True:
    #     return redirect(url_for('dashboard.render_dashboard'))
    form = RegForm()

    if request.method == 'POST':
        print(request.form.get('checkbox'))
        if form.validate():
            check_user = User.getUser(email=form.email.data)
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('dashboard.render_dashboard'))
                    #return redirect(url_for('dashboard'))
                else:
                    form.password.errors.append("User Password entered is incorrect.")
            else:
                form.email.errors.append("No Such User")


    return render_template('login.html', form=form, panel="Login")

@auth.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
