from flask import Flask, url_for, request, render_template, json, redirect, abort
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from data import db_session
from data.users import User
from data.news import News
from data.LoginForm import LoginForm
from data.RegisterForm import RegisterForm
from data.NewsForm import NewsForm
from data.AcceptForm import AcceptForm
from data.AdminForm import AdminForm
from data.RedacuserForm import RedacuserForm
from random import choice
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from validate_email import validate_email

chars = 'abcdefghijklnopqrstuvwxyz1234567890'
spisok_obyazatelnih_symvolov = '(.,:;?!*+%-@[]{}/\_$#)'
spisok_vozmojnih_symvolov = chars + spisok_obyazatelnih_symvolov + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
name_symvols = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя" + chars + \
               "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'  # спросить у учителя
login_manager = LoginManager()
login_manager.init_app(app)


def len_passw(passw):
    if len(passw) < 8 or len(passw) > 24:
        return 0
    else:
        return 1


def bad_symvols(passw):
    bad_symvol = False
    for i in passw:
        if i not in spisok_vozmojnih_symvolov:
            bad_symvol = True
    if bad_symvol:
        return 0
    else:
        return 1


def registr(passw):
    upper = False
    lower = False
    for i in passw:
        if i.isupper():
            upper = True
        elif i.islower():
            lower = True
    if not upper or not lower:
        return 0
    else:
        return 1


def digit(passw):
    digit = False
    wordd = False
    for i in passw:
        if i.isdigit():
            digit = True
        elif i in "abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            wordd = True
    if not digit or not wordd:
        return 0
    else:
        return 1


def must_symvols(passw):
    must = False
    wordd = False
    for i in passw:
        if i in spisok_obyazatelnih_symvolov:
            must = True
        elif i in "abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            wordd = True
    if not must or not wordd:
        return 0
    else:
        return 1


def date():
    Dict_Month = {1: "Января", 2: "Февраля", 3: "Марта", 4: "Апреля", 5: "Мая", 6: "Июня",
                  7: "Июля", 8: "Августа", 9: "Сентября", 10: "Октября", 11: "Ноября", 12: "Декабря"}
    DATA = datetime.datetime.now()
    DATA2 = " ".join([str(i) for i in [str(DATA.hour) + ":" + str(DATA.minute),
                                       DATA.day, Dict_Month[DATA.month], DATA.year, "года"]])
    return DATA2


def mailing(to, kod):
    addr_from = "our.baraholki@mail.ru"
    addr_to = to
    password = "bar.bar.bar"

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = 'Подтвердите вашу почту'

    body = "Ваш код подтверждения - {}\n" \
           "Либо вы можете пройти по ссылке, " \
           "чтобы активировать аакаунт - http://127.0.0.1:5000/checkemail/key={}".format(kod, kod)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.mail.ru', 587)
    server.set_debuglevel(True)
    server.starttls()
    server.login(addr_from, password)
    # server.send_message(msg)
    server.quit()


def generator():
    password = ''
    for i in range(12):
        # проверка кода на существование
        password += choice(chars)
    return password


# @app.errorhandler(500)
# def page_not_found(e):
#     return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
def main_page():
    return render_template('main_page.html', title="НАЗВАНИЕ")


@app.route("/goods")
def goods():
    session = db_session.create_session()
    news = session.query(News).filter(News.is_private != True)
    if current_user.is_authenticated:
        news = session.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = session.query(News).filter(News.is_private != True)
    return render_template("index.html", title="Объявления", news=news)


@app.route("/about")
def about():
    return render_template('about.html', title="О нас")


@app.route("/faq")
def faq():
    return render_template('faq.html', title="ЧаВо")


# @app.route("/contacts")
# def contacts():
#     return render_template('contacts.html', title="О нас")


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        passw = form.password.data
        usname = form.name.data
        List_Psw_Lvl = [sum([len_passw(passw), bad_symvols(passw)]),
                        sum([digit(passw), registr(passw), must_symvols(passw)])]
        # print(List_Psw_Lvl)
        for i in usname:
            if i not in name_symvols:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Имя не соответствует требованиям")
        if List_Psw_Lvl[0] != 2:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароль не соответствует требованиям",
                                   lvl=-1)
        # else:
        #     return render_template('register.html', title='Регистрация',
        #                            form=form,
        #                            message="",
        #                            lvl=List_Psw_Lvl[1])
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже существует")

        while True:
            some = generator()
            if not session.query(User).filter(User.uuid == some).first():
                true_uuid = some
                break

        # if validate_email(form.email.data, verify=True):
        user = User(
            name=form.name.data,
            email=form.email.data,
            uuid=true_uuid,
            created_date=date()
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/accept/{}'.format(user.id))
        # else:
        #     return render_template('register.html', title='Регистрация', form=form,
        #                            mailmessage="Такой почты несуществует")

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/accept/<int:id>', methods=['GET', 'POST'])
def accept(id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    mailing(user.email, user.uuid)
    form = AcceptForm()
    if form.validate_on_submit():
        if user and user.uuid == form.check.data:
            user.is_activate = True
            session.commit()
            return redirect('/login')
        else:
            return render_template('accept.html', form=form, message="Неверный код. Попробуйте ещё раз.")

    return render_template('accept.html', title='НАЗВАНИЕ', form=form)


@app.route('/checkemail/key=<string:code>')
def checkemail(code):
    session = db_session.create_session()
    user = session.query(User).filter(User.uuid == code).first()
    user.is_activate = True
    session.commit()



@app.route('/user')
@login_required
def user():
    # session = db_session.create_session()
    # user = session.query(User).filter(User.id == id).first()
    return render_template('user.html', title='личная страница')
    # Если произведён вход, если id входившего равняется id ссылки и акк, на который заходится по ссылке
    # подтверждён, то можно редактировать информацию. В противном случае можно только увидеть информацию.


@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if current_user.id == id:
        form = RedacuserForm()
        if form.validate_on_submit() and form.submit:
            session = db_session.create_session()
            # else:
            #     return render_template('edit_user.html', title='Регистрация',
            #                            form=form,
            #                            message="",
            #                            lvl=List_Psw_Lvl[1])

            if session.query(User).filter(User.email == form.email.data, User.id != id).first():
                return render_template('edit_user.html', title='Редактирование профиля',
                                       form=form,
                                       message="Такой пользователь уже существует")
            user = session.query(User).filter(User.id == id).first()
            if user:

                user.name = form.name.data
                # в html:
                # < !-- < p > -->
                # < !--            {{form.img.label}} < br > -->
                # < !-- & lt;! & ndash; < form
                # method = "POST"
                # enctype = "multipart/form-data" > & ndash; & gt;
                # -->
                # < !-- & lt;! & ndash;
                # {{form.img(type="file")}} < br > & ndash; & gt;
                # -->
                # < !-- & lt;! & ndash; < / form > & ndash; & gt;
                # -->
                # < !--        {{form.img(type="file", method="POST", enctype="multipart/form-data")}} < br > -->
                # < !--            { %
                # for error in form.img.errors %}-->
                # < !-- < div
                #
                # class ="alert alert-danger" role="alert" > -->
                #
                # < !--                    {{error}} -->
                # < !-- < / div > -->
                # < !--            { % endfor %}-->
                # < !-- < / p > -->
                # user.img = form.img.data
                # if form.img.data:
                #     im = Image.open(form.img.data)
                user.contacts = form.contacts.data
                user.email = form.email.data
                print(form.password.data)
                if len(form.password.data) != 0:
                    if not user.check_password(form.old_password.data):
                        return render_template('edit_user.html', title='Редактирование профиля',
                                               form=form,
                                               message="Неверный текущий пароль")
                    if form.old_password.data == form.password.data:
                        return render_template('edit_user.html', title='Редактирование профиля',
                                               form=form,
                                               message="Текущий и новый пароли совпадают")
                    passw = form.password.data
                    List_Psw_Lvl = [sum([len_passw(passw), bad_symvols(passw)]),
                                    sum([digit(passw), registr(passw), must_symvols(passw)])]
                    if List_Psw_Lvl[0] != 2:
                        return render_template('edit_user.html', title='Редактирование профиля',
                                               form=form,
                                               message="Пароль не соответствует требованиям")
                    # user.password = form.password.data
                    user.set_password(form.password.data)
                session.commit()
                return redirect('/user')
            else:
                abort(404)
        return render_template('edit_user.html', title='Редактирование профиля', form=form)
    else:
        abort(404)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.status == "A":
        form = AdminForm()
        session = db_session.create_session()
        users = session.query(User)
        if form.validate_on_submit() and form.id.data != "None":
            print(12)
            try:
                user = session.query(User).filter(User.id == int(form.id.data), User.status != "A").first()
                user.status = "B"
                session.commit()
                return render_template('admin.html', title='личная страница', users=users, form=form)
            except Exception as error:
                print(error)
        return render_template('admin.html', title='личная страница', users=users, form=form)
    else:
        abort(404)

@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html', title='Редактирование новости', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    session = db_session.create_session()
    news = session.query(News).filter(News.id == id,
                                      News.user == current_user).first()
    if news:
        session.delete(news)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            if user.is_activate:
                login_user(user, remember=form.remember_me.data)
                return redirect('/')
            return redirect('/accept/{}'.format(user.id))
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def main():
    db_session.global_init("db/barahol.sqlite")
    app.run()


if __name__ == '__main__':
    main()
