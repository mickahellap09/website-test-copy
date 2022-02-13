from flask import Flask, flash, redirect, render_template, request, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from data import update_databases, main

main.start()

app = Flask(__name__)
app.secret_key = "saldhjaslkjhdlkas"

conn_users = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\users.sqlite3', check_same_thread=False)
cur_users = conn_users.cursor()

conn_banks = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite', check_same_thread=False)
cur_banks = conn_banks.cursor()

cur_banks.execute('SELECT name FROM banks')
all_banks = cur_banks.fetchall()

cur_users.executescript('''

CREATE TABLE IF NOT EXISTS users(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, username TEXT UNIQUE, password TEXT, role INTEGER);

''')

@app.route('/')
def index():
    if "user" in session:
        return render_template('base.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            cur_users.execute(
                'SELECT password FROM users WHERE users.username = (?)', (username,))
            encrypted_password = cur_users.fetchone()[0]
        except:
            flash("Incorrect username.", category='error')
            return render_template('login.html')

        if check_password_hash(encrypted_password, password):
            session['user'] = username
            flash('Login successful.', category='success')
            cur_users.execute(
                'SELECT role FROM users WHERE users.username = ?', (username,))
            session['role'] = cur_users.fetchone()[0]

        else:
            flash('Incorrect password.', category='error')
            return render_template('login.html')

        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():

    if "user" in session:
        session.pop('user')
        session.pop('role')
        flash('Successfully logged out.', category='success')
        return redirect(url_for('login'))
    else:
        flash('Please sign in.')
        return redirect(url_for('login'))


@app.route('/admin/add_new_user', methods=['GET', 'POST'])
def add_new_user():

    if "user" in session:
        user = session['user']
        cur_users.execute(
            'SELECT role FROM users WHERE users.username = ?', (user,))
        role = cur_users.fetchone()[0]
        if role == 0:
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                admin_true = request.form.get('admin')
                type1_true = request.form.get('type1')

                cur_users.execute('SELECT username FROM users')
                all_users = cur_users.fetchall()

                for user in all_users:
                    user = user[0]
                    if user == username:
                        flash('This username already exists.', category='error')
                        return render_template('add_new_user.html')
                    else:
                        pass

                password = generate_password_hash(password, method='sha256')

                if admin_true == 'on':
                    role = 0
                elif type1_true == 'on':
                    role = 1
                else:
                    flash('Please select 1 of the tickboxes.', category='error')
                    return render_template('add_new_user.html')

                cur_users.execute('INSERT INTO users(username, password, role) VALUES (?,?,?)',
                                  (username, password, role))
                conn_users.commit()

                flash('User added successfully.', category='success')

                return render_template('add_new_user.html')

            else:
                return render_template('add_new_user.html')
        else:
            flash('You are not authorized to access this page.', category='error')
            return redirect(url_for('index'))
    else:
        flash('Please login to access this page.', category='error')
        return redirect(url_for('login'))


@app.route('/finance/reports')
def reports():

    global check_if_rate
    
    if "user" in session:
        for bank_name in all_banks:
            bank_name = bank_name[0]
            
            check_if_rate = update_databases.check_conventional(bank_name)
        if check_if_rate == True:
            return(redirect(url_for('new_rate')))
        else:

            main.update()

            filepath = r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\reports\bank_data.xlsx'
            os.startfile(filepath)

            return(redirect(url_for('index')))
    else:
        flash('Please login to access this page.', category='error')
        return redirect(url_for('login'))


@app.route('/finance/reports/new_rate', methods=["GET", "POST"])
def new_rate():
    
    global check_if_rate
    
    if request.method == 'POST':
        rate = request.form.get('new_rate')
        rate = float(rate)
        update_databases.add_new_rate_conventional(rate, check_if_rate[1])

        flash('Rate added successfully.', category='success')

        return redirect(url_for('reports'))
    else:
        return render_template('new_rate.html')


@app.route('/finance/bank_borrowing', methods=["GET", "POST"])
def bank_borrowing():
    if "user" in session:
        filepath = r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\debit_form.py'
        os.startfile(filepath)
        return redirect(url_for('index'))
    else:
        flash('Please login to access this page.', category='error')
        return redirect(url_for('login'))


@app.route('/finance/payments')
def payments():
    if "user" in session:
        filepath = r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\payment_form.py'
        os.startfile(filepath)
        return redirect(url_for('index'))
    else:
        flash('Please login to access this page.', category='error')
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
