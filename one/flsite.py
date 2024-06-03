from flask import Flask, render_template, url_for, request, flash, session, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'khfkjy8979878070983hjhdskjhsdkgvsdjjgb4jbht3jb'
menu = [
    {"name": "Главная", "url": "index"},
    {"name": "О нас", "url": "about"},
    {"name": "Обратная связь", "url": "contact"}
]


@app.route("/")
@app.route("/index")
def index():
    print(url_for("index"))
    return render_template('index.html', title='Главная', menu=menu)


@app.route("/about")
def about():
    print(url_for("about"))
    return render_template('about.html', title='О нас', menu=menu)


@app.route("/profile/<username>")
def profile(username):
    return f"Пользователь: {username}"


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        if len(request.form['username']) > 2:
            flash("Сообщение отправлено успешно", category='success')
            print(request.form)
        else:
            flash("Ошибка отправки", category='error')

        # context = {
        #     'username': request.form['username'],
        #     'email': request.form['email'],
        #     'message': request.form['message']
        #
        # }
        # return render_template("contact.html", **context, title='Обратная связь', menu=menu)
    return render_template("contact.html", title='Обратная связь', menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    print(error)
    return render_template("page404.html", title='Станица не найдена', menu=menu)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and request.form['username'] == "admin" and request.form['psw'] == "123456":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template("login.html", title='Авторизация', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
