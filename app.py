from models import db, User
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm
import hashlib
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
app.config['SECRET_KEY'] = b'6d0d6a76c0e1522867f9cc1681db0a5972bd1c30a03834d1af4b71f381698f84'
csrf = CSRFProtect(app)


@app.route('/')
def index():
    return redirect(url_for('registration'))


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        name = form.username.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        print(name, surname, email, password)
        salt = os.urandom(32)
        password_protection = password
        key = hashlib.pbkdf2_hmac('sha256', password_protection.encode('utf-8'), salt, 100000, dklen=128)
        user = User(username=name, surname=surname, email=email, password=key)
        db.session.add(user)
        db.session.commit()
        return f'Пользователь {name} добавлен в базу'
    return render_template('registration.html', form=form)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('Таблица создана')


if __name__ == '__main__':
    app.run(debug=True)
