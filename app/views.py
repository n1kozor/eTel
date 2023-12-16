# views.py
from flask import request, jsonify
from flask import render_template, flash, redirect, url_for, session
from flask_login import current_user, login_user, LoginManager, logout_user, login_required
from app import app
from app.forms import LoginForm
from app.methods import UserMethods, BankAccountMethods, TransactionMethods
from app.models import User, BankAccount, Transaction

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    # Ide jön a felhasználó betöltésének logikája
    return User.query.get(int(user_id))

# ha az indexre erkezel, akkor rögtön a loginra redirectel
@app.route('/')
def index():
    return redirect(url_for('login'))

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
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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
    sum = BankAccountMethods.sum_all(user=current_user)

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

        elif request.form.get('edit'):
            bank_account_id = request.form.get('bank_account_id')
            bank_account = BankAccountMethods.get_by_id(bank_account_id)
            if bank_account:
                BankAccountMethods.update(bank_account, user=current_user,
                                          bank_name=request.form.get('bank_name'),
                                          account_number=request.form.get('account_number'),
                                          account_type=request.form.get('account_type'),
                                          balance=request.form.get('balance'))
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
    if request.method == 'POST':
        if request.form.get('add'):
            bank_account_id = request.form.get('bank_account_id')
            amount = request.form.get('amount')
            transaction_type = request.form.get('transaction_type')
            description = request.form.get('description')
            TransactionMethods.add(bank_account_id, amount, transaction_type, description)


            return redirect(url_for('transactions'))


        elif request.form.get('edit'):
            transaction_id = request.form.get('transaction_id')
            bank_account = request.form.get('bank_account_id')
            amount = request.form.get('amount')
            transaction_type = request.form.get('transaction_type')
            description = request.form.get('description')
            TransactionMethods.update(transaction_id, bank_account, amount, transaction_type, description)
            return redirect(url_for('transactions'))


    chart_data = {}
    for bank_account in current_user.bank_accounts:
        transactions = bank_account.transactions
        dates = [transaction.created_at.strftime("%Y-%m-%d") for transaction in transactions]
        balances = [transaction.actual_balance for transaction in transactions]
        chart_data[bank_account.id] = {'dates': dates, 'balances': balances}


    chart_series = []
    for bank_account in current_user.bank_accounts:
        account_data = {
            'name': f"{current_user.username}'s {bank_account.bank_name}",
            'data': [[transaction.created_at.strftime("%Y-%m-%d"), transaction.actual_balance] for transaction in
                     bank_account.transactions]
        }
        chart_series.append(account_data)

    return render_template('transactions.html', title='Transactions', chart_data=chart_data, chart_series=chart_series)

@app.route('/charts_bank')
def charts_bank():
    chart_income_expense = {}
    for bank_account in current_user.bank_accounts:
        income = sum([t.amount for t in bank_account.transactions if t.transaction_type == 'deposit'])
        expense = sum([t.amount for t in bank_account.transactions if t.transaction_type == 'withdrawal'])
        bank_name = bank_account.bank_name
        chart_income_expense[bank_account.id] = {'bank_name': bank_name, 'income': income, 'expense': expense}

    chart_transaction_count = {}
    for bank_account in current_user.bank_accounts:
        transactions_count = len(bank_account.transactions)
        bank_name = bank_account.bank_name
        chart_transaction_count[bank_account.id] = {'bank_name': bank_name, 'transactions_count': transactions_count}

    chart_transaction_time = {}
    for bank_account in current_user.bank_accounts:
        transactions = bank_account.transactions
        dates = [transaction.created_at.strftime("%Y-%m-%d") for transaction in transactions]
        balances = [transaction.actual_balance for transaction in transactions]
        bank_name = bank_account.bank_name
        chart_transaction_time[bank_account.id] = {'dates': dates, 'balances': balances, 'bank_name': bank_name}
    return render_template('charts_bank.html', chart_transaction_time=chart_transaction_time, chart_income_expense=chart_income_expense, chart_transaction_count=chart_transaction_count)



############################################


@app.route('/last-transactions', methods=['GET', 'POST'])
@login_required
def last_transactions():
    user = current_user
    all_transactions = UserMethods.get_all_transactions(user)

    # Flatten transactions
    flat_transactions = [trans for account_transactions in all_transactions.values() for trans in account_transactions]

    # Sort by 'created_at' key in the dictionaries
    flat_transactions.sort(key=lambda x: x['created_at'], reverse=True)

    # Get the last five transactions
    last_five = flat_transactions[:5]

    return jsonify(last_five)


