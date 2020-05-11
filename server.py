from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_ngrok import run_with_ngrok
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import PasswordField, BooleanField, SubmitField, StringField, TextAreaField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

import purchases_resources
import users_resources

from data import db_session
from data.users import User, Purchases

from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
run_with_ngrok(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/lists.sqlite")


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


# изменить
class PurchasesForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    count = IntegerField('Количество')
    content = TextAreaField("Дополнение")
    submit = SubmitField('Готово!')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
def index():
    session = db_session.create_session()
    purchases = session.query(Purchases)
    print(request.path)
    return render_template("index.html", purchases=purchases)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/purchases', methods=['GET', 'POST'])
@login_required
def add_purchases():
    form = PurchasesForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        purchases = Purchases()
        purchases.title = form.title.data
        purchases.count = form.count.data
        purchases.content = form.content.data
        current_user.purchases.append(purchases)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('purchases.html', title='Добавление покупки',
                           form=form)


@app.route('/purchases/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_purchases(id):
    form = PurchasesForm()
    if request.method == "GET":
        session = db_session.create_session()
        purchases = session.query(Purchases).filter(Purchases.id == id,
                                                    Purchases.user == current_user).first()
        if purchases:
            form.title.data = purchases.title
            form.content.data = purchases.content
            form.count.data = purchases.count
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        purchases = session.query(Purchases).filter(Purchases.id == id,
                                                    Purchases.user == current_user).first()
        if purchases:
            purchases.title = form.title.data
            purchases.content = form.content.data
            purchases.count = form.count.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    print(request.path[:-1])
    return render_template('purchases.html', title='Редактирование покупки', form=form)


@app.route('/purchases_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def purchases_delete(id):
    session = db_session.create_session()
    purchases = session.query(Purchases).filter(Purchases.id == id,
                                                Purchases.user == current_user).first()
    if purchases:
        session.delete(purchases)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.sqlite")
    # app.register_blueprint(purchases_api.blueprint)
    app.run()


if __name__ == '__main__':
    # adding purchases
    # для списка объектов
    api.add_resource(purchases_resources.PurchasesListResource, '/api/purchases')
    #
    # # для одного объекта
    api.add_resource(purchases_resources.PurchasesResource, '/api/purchases/<int:purchases_id>')
    # adding uers
    api.add_resource(users_resources.UsersListResource, '/api/users')
    #
    # # для одного объекта
    api.add_resource(users_resources.UsersResource, '/api/users/<int:users_id>')

    main()
