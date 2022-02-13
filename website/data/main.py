import sqlite3

from openpyxl import Workbook
    
def update():
    
    from . import update_databases, create_reports

    conn_banks = sqlite3.connect(
        r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite', check_same_thread=False)
    cur_banks = conn_banks.cursor()

    cur_banks.execute('SELECT name FROM banks')
    all_banks = cur_banks.fetchall()
    
    for bank_name in all_banks:
        bank_name = bank_name[0]
        
        update_databases.input_dates(bank_name)
        update_databases.update_view(bank_name)
    create_reports.update_sheets()
    
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