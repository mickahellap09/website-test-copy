import sqlite3
import update_databases

conn_banks = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite', check_same_thread=False)
cur_banks = conn_banks.cursor()

def start():
    conn_banks = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite', check_same_thread=False)
    cur_banks = conn_banks.cursor()
    
    cur_banks.executescript('''CREATE TABLE IF NOT EXISTS bank_types(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, type TEXT UNIQUE);

    CREATE TABLE IF NOT EXISTS banks(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT UNIQUE, bank_type_id INTEGER NOT NULL)

    ''')
    try:
        cur_banks.execute('INSERT INTO bank_types(type) VALUES (?)', ('conventional',))
        cur_banks.execute('INSERT INTO bank_types(type) VALUES (?)', ('islamic',))
    except:pass

    conn_banks.commit()

def add_new_bank(bank_name, bank_type, date):

    bank_name = bank_name.upper()

    path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()
    
    cur_banks.execute('SELECT id FROM bank_types WHERE bank_types.type = (?)', (bank_type,))
    bank_type_id = cur_banks.fetchone()[0]

    cur_banks.execute('SELECT id FROM bank_types WHERE bank_types.type = (?)', ('conventional',))
    conventional_id = cur_banks.fetchone()[0]

    cur_banks.execute('SELECT id FROM bank_types WHERE bank_types.type = (?)', ('islamic',))
    islamic_id = cur_banks.fetchone()[0]

    if bank_type_id == conventional_id:
        cur.executescript('''

        CREATE TABLE IF NOT EXISTS transaction_types(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, type TEXT UNIQUE);

        CREATE TABLE IF NOT EXISTS debit_credit(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, type TEXT UNIQUE);

        CREATE TABLE IF NOT EXISTS dates(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, date TEXT UNIQUE);

        CREATE TABLE IF NOT EXISTS rates(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, rate DECIMAL, date_id INTEGER NOT NULL);

        CREATE TABLE IF NOT EXISTS transactions(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, transaction_type_id INTEGER, debit_credit_id INTEGER, date_id INTEGER NOT NULL, amount INTEGER NOT NULL);

        CREATE TABLE IF NOT EXISTS view(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, date_id INTEGER NOT NULL, rate_id INTEGER, principal_debit INTEGER, principal_credit INTEGER, principal_balance INTEGER, markup_debit INTEGER, markup_credit INTEGER, markup_balance INTEGER);

        ''')
    elif bank_type_id == islamic_id:
        cur.executescript('''

        CREATE TABLE IF NOT EXISTS transaction_types(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, type TEXT UNIQUE);

        CREATE TABLE IF NOT EXISTS debit_credit(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, type TEXT UNIQUE);

        CREATE TABLE IF NOT EXISTS dates(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, date TEXT UNIQUE);

        CREATE TABLE IF NOT EXISTS transactions(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, transaction_type_id INTEGER, debit_credit_id INTEGER, date_id INTEGER NOT NULL, amount INTEGER NOT NULL, rate DECIMAL);

        CREATE TABLE IF NOT EXISTS view(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, date_id INTEGER NOT NULL, rate_id INTEGER, principal_debit INTEGER, principal_credit INTEGER, principal_balance INTEGER, markup_debit INTEGER, markup_credit INTEGER, markup_balance INTEGER);

        ''')

    cur_banks.execute('INSERT INTO banks(name, bank_type_id) VALUES (?,?)', (bank_name, bank_type_id,))

    cur.execute('INSERT INTO transaction_types(type) VALUES (?)', ('principal',))
    cur.execute('INSERT INTO transaction_types(type) VALUES (?)', ('markup',))

    cur.execute('INSERT INTO debit_credit(type) VALUES (?)', ('debit',))
    cur.execute('INSERT INTO debit_credit(type) VALUES (?)', ('credit',))

    cur.execute('INSERT INTO dates(date) VALUES (?)', (date,))

    conn.commit()

    update_databases.input_dates(bank_name)

    conn.commit()
    conn_banks.commit()
    conn_banks.close()
    conn.close()