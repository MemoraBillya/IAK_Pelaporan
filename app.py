from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Konfigurasi database MySQL
app.secret_key = 'your_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pelaporan'

# Inisialisasi MySQL
mysql = MySQL(app)

# Route untuk halaman login
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        
        # Memeriksa user di database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        account = cursor.fetchone()
        
        # Jika akun ditemukan
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect email/password!'
    return render_template('login.html', msg=msg)

# Route untuk halaman register
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Memeriksa apakah user sudah ada
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not name or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Jika tidak ada error, simpan user ke database
            cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (name, email, password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('login.html', msg=msg)

# Route untuk halaman utama setelah login
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

# Route untuk logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))

# Route untuk halaman Supplier
@app.route('/supplier')
def supplier():
    if 'loggedin' in session:
        return render_template('supplier.html')
    return redirect(url_for('login'))

# Route untuk halaman Distributor
@app.route('/distributor')
def distributor():
    if 'loggedin' in session:
        return render_template('distributor.html')
    return redirect(url_for('login'))

# Route untuk halaman Retail
@app.route('/retail')
def retail():
    if 'loggedin' in session:
        return render_template('retail.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
