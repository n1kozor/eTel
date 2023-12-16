# methods.py
from app import db, app
from app.models import User, BankAccount, Transaction


class UserMethods:

    @staticmethod
    def add_user(username, email, password, country, zipcode, city, address, phone, gender, is_active=True, is_admin=False):
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                return None
            new_user = User(
                username=username,
                email=email,
                country=country,
                zipcode=zipcode,
                city=city,
                address=address,
                phone=phone,
                gender=gender,
                is_active=is_active,
                is_admin=is_admin
            )
            new_user.set_password(password)  # Jelszó hashelés helyesen
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            app.logger.error(e)
            return None
    @staticmethod
    def get_user_by_id(user_id):
        try:
            return User.query.get(user_id).first()
        except Exception as e:
            app.logger.error(e)
            return None
    @staticmethod
    def get_user_by_username(username):
        try:
            return User.query.filter_by(username=username).first()
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def update_user(user, **kwargs):
        try:
            if not user:
                return False

            for key, value in kwargs.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
                    if key == 'password_hash':
                        user.set_password(value)

            db.session.commit()
            return True
        except Exception as e:
            app.logger.error(e)
            return False


    @staticmethod
    def delete_user(user_id):
        try:
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            return False
        except Exception as e:
            app.logger.error(e)
            return False

    @staticmethod
    def get_all_users():
        try:
            return User.query.all()
        except Exception as e:
            app.logger.error(e)
            return None
    @staticmethod
    def get_users_bank_accounts(user):
        try:
            return user.bank_accounts
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def get_user_by_email(email):
        try:
            return User.query.filter_by(email=email).first()
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def get_user_by_phone(phone):
        try:
            return User.query.filter_by(phone=phone).first()
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def get_user_by_country(country):
        try:
            return User.query.filter_by(country=country).first()
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def get_user_by_zipcode(zipcode):
        try:
            return User.query.filter_by(zipcode=zipcode).first()
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def get_user_by_city(city):
        try:
            return User.query.filter_by(city=city).first()
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def set_admin(user):
        try:
            user.is_admin = True
            db.session.commit()
            return True
        except Exception as e:
            app.logger.error(e)
            return False

    @staticmethod
    def get_all_transactions(user):
        try:
            transactions_by_account = {}
            for bank_account in user.bank_accounts:
                transactions_by_account[bank_account.id] = [transaction.to_dict() for transaction in
                                                            bank_account.transactions]
            return transactions_by_account
        except Exception as e:
            app.logger.error("Error in get_all_transactions: %s", str(e))
            return {}

class BankAccountMethods:
    @staticmethod
    def add(bank_name, account_number, account_type, balance, user):
        try:
            if user:
                new_bank_account = BankAccount(
                    bank_name=bank_name,
                    account_number=account_number,
                    account_type=account_type,
                    balance=balance,
                    is_active=True
                )
                user.bank_accounts.append(new_bank_account)
                db.session.add(new_bank_account)
                db.session.commit()
                return new_bank_account
            return None
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def get_all():
        try:
            return BankAccount.query.all()
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def get_by_user(user):
        try:
            return user.bank_accounts
        except Exception as e:
            app.logger.error(e)
            return None
    @staticmethod
    def get_by_id(bank_account_id):
        try:
            return BankAccount.query.filter_by(id=bank_account_id).first()
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def update(bank_account, bank_name=None, account_number=None, account_type=None, balance=None, user=None):
        try:
            if bank_account:
                if bank_name is not None:
                    bank_account.bank_name = bank_name
                if account_number is not None:
                    bank_account.account_number = account_number
                if account_type is not None:
                    bank_account.account_type = account_type
                if balance is not None:
                    bank_account.balance = balance
                bank_account.user = user


                bank_account.updated_at = db.func.current_timestamp()
                db.session.commit()
                return bank_account
            return None
        except Exception as e:
            app.logger.error(e)
            return None

    # set inactive
    @staticmethod
    def set_inactive(bank_account_id):
        try:
            bank_account = BankAccount.query.filter_by(id=bank_account_id).first()
            if bank_account:
                bank_account.is_active = False
                db.session.commit()
                return True
            return False
        except Exception as e:
            print(e)
            app.logger.error(e)
            return False
    @staticmethod
    def set_active(bank_account_id):
        try:
            bank_account = BankAccount.query.filter_by(id=bank_account_id).first()
            if bank_account:
                bank_account.is_active = True
                db.session.commit()
                return True
            return False
        except Exception as e:
            print(e)
            app.logger.error(e)
            return False
    @staticmethod
    def add_user_to_bank_account(user, bank_account):
        try:
            if user and bank_account:
                user.bank_accounts.append(bank_account)
                db.session.commit()
                return True
            return False
        except Exception as e:
            app.logger.error(e)
            return False

    @staticmethod
    def change_balance(bank_account_id, balance):
        try:
            bank_account = BankAccountMethods.get_bank_account_by_id(bank_account_id)
            if bank_account:
                bank_account.balance = balance
                db.session.commit()
                return True
            return False
        except Exception as e:
            app.logger.error(e)
            return False

    @staticmethod
    def delete_user_from_bank_account(user, bank_account):
        try:
            if user and bank_account in user.bank_accounts:
                user.bank_accounts.remove(bank_account)
                db.session.commit()
                return True
            return False
        except Exception as e:
            app.logger.error(e)
            return False
    @staticmethod
    def deposit(bank_account, amount):
        try:
            if bank_account:
                bank_account.balance += float(amount)
                db.session.commit()
                return True
            return False
        except Exception as e:
            app.logger.error(e)
            return False

    @staticmethod
    def withdraw(bank_account, amount):
        try:
            if bank_account:
                bank_account.balance -= float(amount)
                db.session.commit()
                return True
            return False
        except Exception as e:
            app.logger.error(e)
            return False

    # Sum all bank account balances
    @staticmethod
    def sum_all(user):
        bank_account = BankAccountMethods.get_by_user(user)
        sum_all = sum(i.balance for i in bank_account)
        try:
            return sum_all
        except Exception as e:
            app.logger.error(e)
            return None


class TransactionMethods:
    @staticmethod
    def add(bank_account_id, amount, transaction_type, description):
        try:
            bank_account_id = int(bank_account_id)
            amount = float(amount)

            bank_account = BankAccount.query.get(bank_account_id)
            if bank_account:

                new_transaction = Transaction(
                    bank_account=bank_account,
                    amount=amount,
                    transaction_type=transaction_type,
                    description=description,
                    actual_balance=0
                )

                db.session.add(new_transaction)

                if transaction_type == 'deposit':
                    BankAccountMethods.deposit(bank_account, amount)
                elif transaction_type == 'withdrawal':
                    BankAccountMethods.withdraw(bank_account, amount)

                new_transaction.actual_balance = bank_account.balance

                db.session.commit()
                return new_transaction
            else:
                return None
        except Exception as e:
            app.logger.error(e)
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_all():
        try:
            return Transaction.query.all()
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def get_by_bank_account(bank_account):
        try:
            return bank_account.transactions
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def get_by_id(transaction_id):
        try:
            return Transaction.query.get(transaction_id)
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def update(transaction_id, **kwargs):
        try:
            transaction = Transaction.query.get(transaction_id)
            if transaction:
                for key, value in kwargs.items():
                    if hasattr(transaction, key):
                        setattr(transaction, key, value)
                db.session.commit()
                return transaction
            return None
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def delete(transaction):
        try:
            if transaction:
                db.session.delete(transaction)
                db.session.commit()
                return True
            return False
        except Exception as e:
            app.logger.error(e)
            return False







# with app.app_context():
#     bankaccount = BankAccountMethods.get_bank_account_by_id(1)
#     print(bankaccount.balance)
#     TransactionMethods.add_transaction(bankaccount, 1000, 'deposit', 'Deposit 1000')





