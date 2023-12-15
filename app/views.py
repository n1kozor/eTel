# views.py

from flask import render_template, flash, redirect, url_for, session
from flask_login import current_user, login_user, LoginManager, logout_user, login_required
from app import app
from app.forms import LoginForm
from app.methods import UserMethods, BankAccountMethods
from app.models import User

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    # Ide jön a felhasználó betöltésének logikája
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('login.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('dashboard'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))


from flask import request


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        country = request.form.get('country')
        zipcode = request.form.get('zipcode')
        city = request.form.get('city')
        address = request.form.get('address')
        phone = request.form.get('phone')
        gender = request.form.get('gender')

        user = UserMethods.add_user(username, email, password, country, zipcode, city, address, phone, gender,
                                    is_active=True, is_admin=False)
        print(user)
        if user:
            flash('Registration successful!')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.')

    return render_template('register.html', title='Register')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.password = request.form['password']
        current_user.email = request.form['email']
        current_user.country = request.form['country']
        current_user.zipcode = request.form['zipcode']
        current_user.city = request.form['city']
        current_user.address = request.form['address']
        current_user.phone = request.form['phone']
        current_user.gender = request.form['gender']

        UserMethods.update_user(user=current_user, password_hash=current_user.password, email=current_user.email
                                , country=current_user.country, zipcode=current_user.zipcode, city=current_user.city,
                                address=current_user.address, phone=current_user.phone, gender=current_user.gender)
        return redirect(url_for('profile'))

    return render_template('profile.html', title='Profile', user=current_user)


@app.route('/bankaccounts', methods=['GET', 'POST', 'DELETE'])
@login_required
def bankaccounts():
    sum = BankAccountMethods.sum_all()
    if request.method == 'POST':
        if request.form.get('deactivate'):
            bank_account = request.form.get('bank_account_id')
            if bank_account:
                BankAccountMethods.set_inactive(bank_account)
                return redirect(url_for('bankaccounts'))

        elif request.form.get('activate'):
            bank_account = request.form.get('bank_account_id')
            if bank_account:
                BankAccountMethods.set_active(bank_account)
                return redirect(url_for('bankaccounts'))

        else:
            bank_name = request.form.get('bank_name')
            account_number = request.form.get('account_number')
            account_type = request.form.get('account_type')
            balance = request.form.get('balance')
            BankAccountMethods.add(bank_name, account_number, account_type, balance, current_user)
            return redirect(url_for('bankaccounts'))
    return render_template('bankaccounts.html', title='Bank Accounts', sum=sum)

@app.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():


    return render_template('transactions.html', title='Transactions')
