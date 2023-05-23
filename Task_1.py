from flask import Flask, render_template, request, flash, url_for, make_response
from pathlib import PurePath, Path

from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename, redirect
from markupsafe import escape


app = Flask(__name__)

users = ['Jonh', 'Olga', 'Smith']
info = {
    'Jonh': '123',
    'Olga': 'qwerty',
    'Smith': "12345"
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello/')
def hello():
    name = 'Bob'
    return f'Hello, {name}'


@app.get('/upload/')
def image_get():
    return render_template('upload.html')


@app.post('/upload/')
def image_post():
    file = request.files.get('file')
    file_name = secure_filename(file.filename)
    file.save(PurePath.joinpath(Path.cwd(), 'uploads', file_name))
    return f'Файл {file_name} загружен на сервер'


@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and password == info[username]:
            return f'Hello, {username}'
    return render_template('login.html')


@app.route('/words/', methods=['GET','POST'])
def words_count():
    if request.method == 'POST':
        words = escape(request.form.get('words').split())
        return f'Коичество слов равно {len(words)}'
    return render_template('words.html')


@app.route('/operations/', methods=['GET','POST'])
def operations():
    if request.method == 'POST':
        num1 = int(escape(request.form.get('num1')))
        num2 = int(escape(request.form.get('num2')))
        operation = escape(request.form.get('operation'))

        if operation == '+':
            return f'Сумма: {num1 + num2} '
        if operation == '-':
            return f'Остаток: {num1 - num2} '
        if operation == '*':
            return f' Произведение: {num1 * num2} '
        if operation == '/':
            return f'Частное: {num1 / num2} '
    return render_template('operations.html')


@app.route('/age/', methods=['GET','POST'])
def age():
    AGE = 18
    if request.method == 'POST':
        age = int(escape(request.form.get('age')))
        if age < AGE:
            abort(403)
        return f'Возраст {age} старше {AGE}'
    return render_template('age.html')


@app.errorhandler(403)
def not_allow(e):
    return render_template('403.html'), 403


@app.route('/square/<numb>')
def square(numb):
    return f'Квадрат числа {int(numb)} равен {int(numb)*int(numb)}!'


@app.route('/redirect/', methods=['GET','POST'])
def redirect_to_square():
    if request.method == 'POST':
        numb = int(escape(request.form.get('numb')))
        return redirect(url_for('square', numb=numb))
    return render_template('square.html')


app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = escape(request.form.get('name'))
        flash(f'Привет, {name}!', 'success')
        return redirect(url_for('form'))
    return render_template('form.html')


@app.route('/hello_user/<username>')
def hello_user(username):
    return render_template('hello_user.html', username=username)


@app.route('/email/', methods=['GET','POST'])
def email():
    if request.method == 'POST':
        username = request.form.get('username')
        user_email = request.form.get('email')
        response = make_response(redirect(url_for('hello_user', username=username)))
        response.set_cookie(username, user_email)
        return response
    return render_template('email.html')


if __name__ == '__main__':
    app.run()