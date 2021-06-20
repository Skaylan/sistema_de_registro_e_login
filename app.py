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
    if 'user' in session:
        return redirect(url_for('user'))
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
        db = sqlite3.connect('todo.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {user};")
        todo_list = cursor.fetchall()
        cursor.close()
        print(session['user'])
            
        return render_template('user.html', user=user, todo=todo_list)
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
            cursor.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)')
            try:
                cursor.execute('INSERT INTO users VALUES(NULL, ?, ?)', (username, password))
                flash('Registrado com sucesso, agora você pode logar!')
            except Exception as erro:
                if erro.__cause__ == None:
                    flash('Usuario já existe, tente outro.')
            db.commit()

            db2 = sqlite3.connect('todo.db')
            cursor2 = db2.cursor()
            cursor2.execute(f"CREATE TABLE IF NOT EXISTS {username}(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,todo TEXT NOT NULL,createdAt DATETIME DEFAULT(GETDATE()))")
            db2.commit()

    return render_template('register.html')



@app.route('/post', methods=['GET', 'POST'])
def post():
    db = sqlite3.connect('todo.db')
    cursor = db.cursor()

    if request.method == 'POST':
        todo = request.form['add-todo']
        print(todo)
        cursor.execute(f"INSERT INTO {session['user']} VALUES(NULL, ?, date('now'))", (todo,))
        cursor.close()
        db.commit()
        return redirect(url_for('user'))


@app.route('/deletar', methods=['POST'])
def deletar():
    if request.method == 'POST':
        req = request.form['deletar']
        print(req)
        db = sqlite3.connect('todo.db')
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM todo WHERE id='{req}'")
        cursor.close()
        db.commit()
        return redirect(url_for('user'))

if __name__ == '__main__':
    app.run(debug=True)
