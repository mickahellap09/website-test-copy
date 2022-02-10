import sqlite3

conn_banks = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite', check_same_thread=False)
cur_banks = conn_banks.cursor()

cur_banks.executescript(
    '''CREATE TABLE IF NOT EXISTS BANKS(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT);''')


def create_tables(bank_name):
    bank_name = bank_name[0]

    path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name.upper()}_bank_data.sqlite'
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.executescript('''CREATE TABLE IF NOT EXISTS DATES(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, date TEXT UNIQUE);

    CREATE TABLE IF NOT EXISTS PRINCIPAL(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, date_id, rate DECIMAL, debit INTEGER, credit INTEGER, balance INTEGER);

    CREATE TABLE IF NOT EXISTS MARKUP(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, date_id, debit DECIMAL, credit DECIMAL, balance DECIMAL);

    ''')

    conn.commit()
    conn.close()


def create():
    cur_banks.execute('SELECT name FROM BANKS')
    all_bank_names = cur_banks.fetchall()
    for name in all_bank_names:
        create_tables(name)


def add_new_bank(name, rate, date):
    name = name.upper().strip()
    cur_banks.execute('INSERT INTO BANKS (name) VALUES (?)', (name,))
    conn_banks.commit()

    create()

    path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{name}_bank_data.sqlite'
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.execute('INSERT INTO DATES(date) VALUES (?)', (date,))
    cur.execute('SELECT id FROM DATES WHERE DATES.date = (?)', (date,))
    date_id = cur.fetchone()[0]

    cur.execute(
        'INSERT INTO PRINCIPAL (date_id, rate, debit, balance) VALUES (?,?,?,?)', (date_id, rate, 0, 0,))

    conn.commit()
