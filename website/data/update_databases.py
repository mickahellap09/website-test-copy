import sqlite3
from datetime import datetime, timedelta
import datetime

conn_banks = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite', check_same_thread=False)
cur_banks = conn_banks.cursor()

def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days


def input_dates(bank_name):
    path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    currentdate = datetime.date.today()

    cur.execute('SELECT date FROM dates ORDER BY id ASC LIMIT 1')
    start_date = cur.fetchone()[0]
    start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y').date()

    all_dates = date_range(start_date, currentdate)

    for date in all_dates:
        date = date.strftime('%d/%m/%Y')
        try:
            cur.execute('INSERT INTO dates(date) VALUES (?)', (date,))
        except:
            pass
    conn.commit()
    conn.close()

def add_new_transaction_debit_conventional(bank_name, transaction_type, debit_or_credit, amount, date):
    path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.execute('SELECT id FROM transaction_types WHERE transaction_types.type = (?)', (transaction_type,))
    transaction_type_id = cur.fetchone()[0]

    cur.execute('SELECT id FROM debit_credit WHERE debit_credit.type = (?)', (debit_or_credit,))
    debit_credit_id = cur.fetchone()[0]

    cur.execute('SELECT id FROM dates WHERE dates.date = (?)', (date,))
    date_id = cur.fetchone()[0]

    cur.execute('INSERT INTO transactions(transaction_type_id, debit_credit_id, date_id, amount) VALUES (?,?,?,?)',(transaction_type_id, debit_credit_id, date_id, amount,))
    
    conn.commit()
    conn.close()


def add_new_transaction_debit_islamic(bank_name, transaction_type, debit_or_credit, rate, amount, date):
    path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.execute('SELECT id FROM transaction_types WHERE transaction_types.type = (?)', (transaction_type,))
    transaction_type_id = cur.fetchone()[0]

    cur.execute('SELECT id FROM debit_credit WHERE debit_credit.type = (?)', (debit_or_credit,))
    debit_credit_id = cur.fetchone()[0]

    cur.execute('SELECT id FROM dates WHERE dates.date = (?)', (date,))
    date_id = cur.fetchone()[0]

    cur.execute('INSERT INTO transactions(transaction_type_id, debit_credit_id, date_id, amount, rate) VALUES (?,?,?,?,?)',(transaction_type_id, debit_credit_id, date_id, amount, rate,))
    
    conn.commit()
    conn.close()

def add_new_transaction_payment(bank_name, transaction_type, debit_or_credit, amount, date):
    path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur.execute('SELECT id FROM transaction_types WHERE transaction_types.type = (?)', (transaction_type,))
    transaction_type_id = cur.fetchone()[0]

    cur.execute('SELECT id FROM debit_credit WHERE debit_credit.type = (?)', (debit_or_credit,))
    debit_credit_id = cur.fetchone()[0]

    cur.execute('SELECT id FROM dates WHERE dates.date = (?)', (date,))
    date_id = cur.fetchone()[0]

    cur.execute('INSERT INTO transactions(transaction_type_id, debit_credit_id, date_id, amount) VALUES (?,?,?,?)',(transaction_type_id, debit_credit_id, date_id, amount,))
    
    conn.commit()
    conn.close()

def markup_debit_formula(rate, amount):
    a1 = rate/365
    a2 = a1/100
    a3 = a2*amount
    return a3

def update_view(bank_name):
    
    path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    cur_banks.execute('SELECT id FROM bank_types WHERE bank_types.type = (?)', ('islamic',))
    islamic_id = cur_banks.fetchone()[0]

    cur_banks.execute('SELECT bank_type_id FROM banks WHERE banks.name = (?)', (bank_name,))
    bank_type_id = cur_banks.fetchone()[0]

    cur.execute('SELECT date FROM dates')
    all_dates = cur.fetchall()

    cur.execute('SELECT date_id FROM view')
    all_date_ids = cur.fetchall()

    cur.execute('SELECT * FROM transactions')
    all_transactions = cur.fetchall()

    cur.execute('SELECT id FROM debit_credit WHERE debit_credit.type = (?)', ('debit',))
    debit_id = cur.fetchone()[0]

    cur.execute('SELECT id FROM debit_credit WHERE debit_credit.type = (?)', ('credit',))
    credit_id = cur.fetchone()[0]

    cur.execute('SELECT id FROM transaction_types WHERE transaction_types.type = (?)', ('principal',))
    principal_id = cur.fetchone()[0]

    cur.execute('SELECT id FROM transaction_types WHERE transaction_types.type = (?)', ('markup',))
    markup_id = cur.fetchone()[0]

    principal_transactions = []
    markup_transactions = []

    if bank_type_id == islamic_id:
        pass
    else:
        cur.execute('SELECT rate FROM rates')
        all_rates = cur.fetchall()

        for rate in all_rates:
            rate = rate[0]
            cur.execute('SELECT date_id FROM rates WHERE rates.rate = (?)', (rate,))
            date_id = cur.fetchone()[0]

            cur.execute('SELECT id FROM rates WHERE rates.rate = (?)', (rate,))
            rate_id = cur.fetchone()[0]

            cur.execute('UPDATE view SET rate_id = (?) WHERE date_id = (?)', (rate_id, date_id,))


    for transaction in all_transactions:
        if transaction[1] == principal_id:
            principal_transactions.append(transaction)
        elif transaction[1] == markup_id:
            markup_transactions.append(transaction)

    for date in all_dates:
        date = date[0]
        cur.execute('SELECT id FROM dates WHERE dates.date = (?)', (date,))
        date_id = cur.fetchone()

        if date_id in all_date_ids:
            pass
        else:
            cur.execute('INSERT INTO view(date_id) VALUES (?)', (date_id))

    #PRINCIPAL CALCULATIONS AND VIEW HERE

    for transaction in principal_transactions:
        if transaction[2] == debit_id:
            if bank_type_id == islamic_id:
                cur.execute('SELECT id FROM transactions WHERE rate = (?)', (transaction[5],))
                rate_id = cur.fetchone()[0]

                cur.execute('UPDATE view SET rate_id = (?) WHERE date_id = (?)', (rate_id, transaction[3],))
            cur.execute('UPDATE view SET principal_debit = (?) WHERE date_id = (?)', (transaction[4], transaction[3],))

        elif transaction[2] == credit_id:
            cur.execute('UPDATE view SET principal_credit = (?) WHERE date_id = (?)', (transaction[4], transaction[3],))

    for date_id in all_date_ids:
        date_id = date_id[0]

        total_principal_balance = 0

        cur.execute('SELECT principal_debit, principal_credit FROM view WHERE date_id <= (?)', (date_id,))
        all_debit_credit = cur.fetchall()

        for value in all_debit_credit:
            if value == (None, None,):
                pass
            else:
                #debit
                if value[1] == None:
                    total_principal_balance +=  value[0]
    
                #credit
                elif value[0] == None:
                    total_principal_balance +=  value[1]

                else:
                    total_principal_balance += value[0]
                    total_principal_balance += value[1]

        cur.execute('UPDATE view SET principal_balance = (?) WHERE date_id = (?)', (total_principal_balance, date_id,))
        conn.commit()

    #MARKUP CALCULATIONS AND VIEW HERE
        for transaction in markup_transactions:
            cur.execute('UPDATE view SET markup_credit = (?) WHERE date_id = (?)', (transaction[4], transaction[3],))

        for date_id in all_date_ids:
            date_id = date_id[0]

            total_debit = 0

            total_credit = 0

            total_markup_balance = 0

            if bank_type_id == islamic_id:

                cur.execute('SELECT rate_id FROM view WHERE date_id <= (?)', (date_id,))
                all_rate_ids = cur.fetchall()

                cur.execute('SELECT principal_credit FROM view WHERE date_id <= (?)', (date_id,))
                all_principal_credit = cur.fetchall()

                for value in all_principal_credit:
                    if value == (None,):
                        pass
                    else:
                        value = value[0]
                        total_credit += value

                for rate_id in all_rate_ids:
                    if rate_id == (None,):
                        pass
                    else:
                        rate_id = rate_id[0]

                        cur.execute('SELECT rate FROM transactions WHERE id = (?)', (rate_id,))
                        rate = cur.fetchone()[0]

                        cur.execute('SELECT amount FROM transactions WHERE id = (?)', (rate_id,))
                        amount = cur.fetchone()[0]

                        if abs(total_credit) > amount:
                            total_credit =total_credit + amount
                            continue
                        
                        elif abs(total_credit) <= amount:
                            amount += total_credit

                        total = markup_debit_formula(rate, amount)

                        total_debit += total

                cur.execute('UPDATE view SET markup_debit = (?) WHERE date_id = (?)',(total_debit, date_id,))
                
                cur.execute('SELECT markup_debit, markup_credit FROM view WHERE date_id <= (?)', (date_id,))
                all_debit_credit = cur.fetchall()
                
                for value in all_debit_credit:
                    if value == (None, None,):
                        pass
                    else:
                        #debit
                        if value[1] == None:
                            total_markup_balance +=  value[0]
                        
                        #credit
                        elif value[0] == None:
                            total_markup_balance +=  value[1]

                        else:
                            total_markup_balance += value[0]
                            total_markup_balance += value[1]
                        
                

                cur.execute('UPDATE view SET markup_balance = (?) WHERE date_id = (?)', (total_markup_balance, date_id,))

            else:
                cur.execute(
                    'SELECT rate_id FROM view WHERE rate_id IS NOT NULL AND date_id <= (?) ORDER BY id DESC LIMIT 1', (date_id,))
                rate_id = cur.fetchone()[0]

                cur.execute('SELECT rate FROM rates WHERE rates.id = (?)', (rate_id,))
                rate = cur.fetchone()[0]

                cur.execute('SELECT principal_debit, principal_credit FROM view WHERE view.date_id <= (?)', (date_id,))
                all_debit_credit = cur.fetchall()
                for value in all_debit_credit:
                    if value == (None, None,):
                        pass
                    else:
                        #debit
                        if value[1] == None:
                            total_markup_balance +=  value[0]
                        
                        #credit
                        elif value[0] == None:
                            total_markup_balance +=  value[1]

                        else:
                            total_markup_balance += value[0]
                            total_markup_balance += value[1]
                    

                value_total = markup_debit_formula(rate, total_markup_balance)
            
                cur.execute('UPDATE view SET markup_debit = (?) WHERE date_id = (?)', (value_total, date_id,))
                
                for date_id in all_date_ids:
                    date_id = date_id[0]
                    total_markup = 0
                    
                    cur.execute('SELECT markup_debit, markup_credit FROM view WHERE view.date_id <= (?)', (date_id,))
                    all_debit_credit = cur.fetchall()
                    
                    for value in all_debit_credit:
                        if value == (None, None,):
                            pass
                        else:
                            if value[1] == None:
                                total_markup +=  value[0]
                            
                            #credit
                            elif value[0] == None:
                                total_markup +=  value[1]

                            else:
                                total_markup += value[0]
                                total_markup += value[1]
                                
                    cur.execute('UPDATE view SET markup_balance = (?) WHERE view.date_id = (?)', (total_markup, date_id,))
                    

    conn.commit()
    conn.close()



def check_conventional(bank_name):

    cur_banks.execute('SELECT id FROM bank_types WHERE bank_types.type = (?)', ('islamic',))
    islamic_id = cur_banks.fetchone()[0]

    cur_banks.execute('SELECT bank_type_id FROM banks WHERE banks.name = (?)', (bank_name,))
    bank_type_id = cur_banks.fetchone()[0]
    
    if bank_type_id == islamic_id:
        return
    
    path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    current_day = datetime.date.today().day

    current_date = datetime.date.today().strftime('%d/%m/%Y')

    cur.execute(
        'SELECT id FROM dates WHERE dates.date = (?)', (current_date,))
    today_date_id = cur.fetchone()[0]

    cur.execute(
        'SELECT rate FROM rates WHERE rates.date_id = (?)', (today_date_id,))
    today_rate = cur.fetchone()

    if current_day == 1 and today_rate == (None,):
        return (True, bank_name)

    else:
        return False


def add_new_rate_conventional(rate, bank_name):
    path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()

    current_date = datetime.date.today().strftime('%d/%m/%Y')

    cur.execute(
        'SELECT id FROM dates WHERE dates.date = (?)', (current_date,))
    today_date_id = cur.fetchone()[0]

    rate = rate + 1.5

    cur.execute(
        'INSERT INTO rates(rate, date_id) VALUES (?,?)', (rate, today_date_id,))
    conn.commit()
    conn.close()
    