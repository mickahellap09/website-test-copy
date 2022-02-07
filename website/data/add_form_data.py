import sqlite3


def payment_form(bank_name, payment_type, amount, date):

    day = date[8:10]
    month = date[5:7]
    year = date[0:4]
    date = day+'/'+month+'/'+year

    if bank_name == '1':
        bank_name = 'Askari'
    elif bank_name == '2':
        bank_name = 'DIBL'
    elif bank_name == '3':
        bank_name = 'HBL'

    if payment_type == '1':
        payment_type = 'Principal'
    elif payment_type == '2':
        payment_type = 'Markup'

    amount = float(amount)
    amount = -abs(amount)

    bank_name = bank_name.upper()
    path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.execute('SELECT id FROM DATES WHERE DATES.date = (?)', (date,))
    date_id = cur.fetchone()[0]

    if payment_type == 'Principal':
        cur.execute(
            'UPDATE PRINCIPAL SET credit = (?) WHERE PRINCIPAL.id = (?)', (amount, date_id,))
    elif payment_type == 'MARKUP':
        cur.execute(
            'UPDATE MARKUP SET credit = (?) WHERE MARKUP.id = (?)', (amount, date_id,))

    conn.commit()
    conn.close()


def debit_form(bank_name, rate, amount, date):
    day = date[8:10]
    month = date[5:7]
    year = date[0:4]
    date = day+'/'+month+'/'+year

    if bank_name == '1':
        bank_name = 'Askari'
    elif bank_name == '2':
        bank_name = 'DIBL'
    elif bank_name == '3':
        bank_name = 'HBL'

    bank_name = bank_name.upper()
    path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.execute('SELECT id FROM DATES WHERE DATES.date = (?)', (date,))
    date_id = cur.fetchone()[0]

    amount = int(amount)

    rate = float(rate)
    rate = rate + 1.5

    cur.execute(
        'UPDATE PRINCIPAL SET debit = (?) WHERE PRINCIPAL.id = (?)', (amount, date_id,))
    cur.execute(
        'UPDATE PRINCIPAL SET rate = (?) WHERE PRINCIPAL.id = (?)', (rate, date_id,))

    conn.commit()
    conn.close()
