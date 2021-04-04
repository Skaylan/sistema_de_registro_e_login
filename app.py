from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from dotenv import load_dotenv
load_dotenv()
import os




app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('user'))
    else:
        r = ''
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            db = sqlite3.connect('database.db')
            cursor = db.cursor()
            cursor.execute("SELECT username, password FROM users WHERE username = '"+username+"' and password = '"+password+"'")
            r = cursor.fetchall()
            print(r)
            for i in r:
                if username == i[0] and password == i[1]:
                    session['user'] = username
                    return redirect(url_for('user'))
            else:
                flash('Usuario e/ou senha incorretos!')
    return render_template('login.html')


@app.route('/user')
def user():
    if 'user' in session:
        user = session['user']
        return render_template('user.html', user=user)
    else:
        return redirect(url_for('login'))

    


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        flash('Você precisa deslogar para acessar essa pagina!')
        return redirect(url_for('user'))
    else:

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            db = sqlite3.connect('database.db')
            cursor = db.cursor()
            try:
                cursor.execute('INSERT INTO USERS VALUES(NULL, ?, ?)', (username, password))
                flash('Registrato com sucesso, agora você pode logar!')
            except Exception as erro:
                if erro.__cause__ == None:
                    flash('Usuario já existe, tente outro.')
            db.commit()
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
