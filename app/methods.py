# methods.py
from app import db, app
from app.models import User, BankAccount


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
    def update_user(user_id, **kwargs):
        try:
            user = User.query.get(user_id)
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                user.updated_at = db.func.current_timestamp()
                db.session.commit()
                return user
            return None
        except Exception as e:
            app.logger.error(e)
            return None

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



class BankAccountMethods:
    @staticmethod
    def add_bank_account(bank_name, account_number, account_type, balance, user):
        try:
            if user:
                new_bank_account = BankAccount(
                    bank_name=bank_name,
                    account_number=account_number,
                    account_type=account_type,
                    balance=balance
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
    def get_all_bank_accounts():
        try:
            return BankAccount.query.all()
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def get_bank_accounts_by_user(user):
        try:
            return user.bank_accounts
        except Exception as e:
            app.logger.error(e)
            return None
    @staticmethod
    def get_bank_account_by_id(bank_account_id):
        try:
            return BankAccount.query.filter_by(id=bank_account_id).first()
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def update_bank_account(bank_account_id, user=None, **kwargs):
        try:
            bank_account = BankAccount.query.get(bank_account_id)
            if bank_account:
                # Frissíti a BankAccount attribútumait
                for key, value in kwargs.items():
                    if hasattr(bank_account, key):
                        setattr(bank_account, key, value)

                # Frissíti a felhasználókat, ha user_ids meg van adva
                if user is not None:
                    current_users = set(bank_account.users)
                    new_users = set(UserMethods.get_user_by_id(uid) for uid in user.id)

                    # Új felhasználók hozzáadása
                    for user in new_users - current_users:
                        if user:
                            bank_account.users.append(user)

                    # Eltávolítja azokat a felhasználókat, akik már nem szerepelnek a listában
                    for user in current_users - new_users:
                        if user:
                            bank_account.users.remove(user)

                bank_account.updated_at = db.func.current_timestamp()
                db.session.commit()
                return bank_account
            return None
        except Exception as e:
            app.logger.error(e)
            return None

    @staticmethod
    def delete_bank_account(bank_account_id):
        try:
            bank_account = BankAccount.query.get(bank_account_id)
            if bank_account:
                db.session.delete(bank_account)
                db.session.commit()
                return True
            return False
        except Exception as e:
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
    def change_bank_account_balance(bank_account_id, balance):
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
                bank_account.balance += amount
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
                bank_account.balance -= amount
                db.session.commit()
                return True
            return False
        except Exception as e:
            app.logger.error(e)
            return False


with app.app_context():

    user = UserMethods.get_user_by_username("asd")
    account = BankAccountMethods.get_bank_account_by_id(1)

    print(account.balance)

    BankAccountMethods.deposit(account, 255.14)
    print(account.balance)




