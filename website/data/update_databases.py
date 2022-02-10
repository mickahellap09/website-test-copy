import sqlite3
from datetime import datetime, timedelta
import datetime
from calendar import monthrange

conn_banks = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite')
cur_banks = conn_banks.cursor()

cur_banks.execute('SELECT name FROM BANKS')
all_banks = cur_banks.fetchall()


def markup_debit_formula(rate, amount):
    a1 = rate/365
    a2 = a1/100
    a3 = a2*amount
    a4 = a3*1
    return a4


def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days


def input_dates():
    for bank_name in all_banks:
        bank_name = bank_name[0]

        path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
        conn = sqlite3.connect(path)
        cur = conn.cursor()

        currentdate = datetime.date.today()

        cur.execute('SELECT date FROM DATES ORDER BY id ASC LIMIT 1')
        start_date = cur.fetchone()[0]
        start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y').date()

        all_dates = date_range(start_date, currentdate)

        for date in all_dates:
            date = date.strftime('%d/%m/%Y')
            try:
                cur.execute('INSERT INTO DATES(date) VALUES (?)', (date,))
            except:
                pass
        conn.commit()
        conn.close()


def principal_calculations():
    for bank_name in all_banks:
        bank_name = bank_name[0]

        path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
        conn = sqlite3.connect(path)
        cur = conn.cursor()

        cur.execute('SELECT date FROM DATES')
        all_dates = cur.fetchall()

        for date in all_dates:
            date = date[0]

            total = 0

            cur.execute(
                'SELECT id FROM DATES WHERE DATES.date = (?)', (date,))
            date_id = cur.fetchone()[0]

            cur.execute(
                'SELECT balance FROM PRINCIPAL WHERE id = (?)', (date_id,))
            balance = cur.fetchone()
            cur.execute(
                    'SELECT debit, credit FROM PRINCIPAL WHERE id BETWEEN 1 AND (?)', (date_id,))
            all_debit_credit = cur.fetchall()

            for value in all_debit_credit:
                if value == (None, None):
                    pass
                else:
                    if value[1] == None:
                        total += value[0]
                    elif value[0] == None:
                        total += value[1]
                    else:
                        total = total + value[0] + value[1]

            if balance == None:
                cur.execute(
                    'INSERT INTO PRINCIPAL (balance, date_id) VALUES (?, ?)', (total, date_id,))
            else:
                cur.execute(
                    'UPDATE PRINCIPAL SET balance = (?) WHERE PRINCIPAL.date_id = (?)', (total,date_id,)
                )


        conn.commit()
        conn.close()


def check_hbl():
    path = 'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\HBL_bank_data.sqlite'
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    current_day = datetime.date.today().day

    current_date = datetime.date.today().strftime('%d/%m/%Y')

    cur.execute(
        'SELECT id FROM DATES WHERE DATES.date = (?)', (current_date,))
    today_date_id = cur.fetchone()[0]

    cur.execute(
        'SELECT rate FROM PRINCIPAL WHERE PRINCIPAL.id = (?)', (today_date_id,))
    today_rate = cur.fetchone()

    if current_day == 1 and today_rate == (None,):
        return True

    else:
        return False


def add_new_rate(rate):
    path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\HBL_bank_data.sqlite'
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    current_date = datetime.date.today().strftime('%d/%m/%Y')

    cur.execute(
        'SELECT id FROM DATES WHERE DATES.date = (?)', (current_date,))
    today_date_id = cur.fetchone()[0]

    rate = rate + 1.5

    cur.execute(
        'UPDATE PRINCIPAL SET rate = (?) WHERE PRINCIPAL.id = (?)', (rate, today_date_id,))
    conn.commit()
    conn.close()


def markup_calculations():
    for bank_name in all_banks:
        bank_name = bank_name[0]

        path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
        conn = sqlite3.connect(path)
        cur = conn.cursor()

        cur.execute('SELECT date FROM DATES')
        all_dates = cur.fetchall()

        total_balance = 0

        for date in all_dates:
            date = date[0]

            total_credit = 0
            total_debit = 0
            total_markup_balance = 0

            cur.execute('SELECT id FROM DATES WHERE DATES.date = (?)', (date,))
            date_id = cur.fetchone()[0]

            cur.execute(
                'SELECT balance FROM MARKUP WHERE id = (?)', (date_id,))
            balance = cur.fetchone()

            cur.execute(
                'SELECT debit, credit FROM PRINCIPAL WHERE id BETWEEN 1 AND (?)', (date_id,))
            all_debit_credit = cur.fetchall()

            for value in all_debit_credit:
                if value == (None, None):
                    pass
                else:
                    if value[1] == None:
                        total_debit += value[0]
                    elif value[0] == None:
                        total_credit += value[1]
                    else:
                        total_debit += value[0]
                        total_credit += value[1]

            if bank_name == 'HBL':
                cur.execute(
                    'SELECT rate FROM PRINCIPAL WHERE rate IS NOT NULL AND id <= (?) ORDER BY id DESC LIMIT 1', (date_id,))
                rate = cur.fetchone()[0]

                total = total_debit + total_credit

                value_total = markup_debit_formula(rate, total)

                total_markup_balance += value_total

            else:
                cur.execute('SELECT debit FROM PRINCIPAL')
                all_debit = cur.fetchall()
                for value in all_debit:
                    if value == (None, None):
                        pass
                    elif value == (None,):
                        pass
                    else:
                        value = value[0]

                        if abs(total_credit) >= value:
                            total_credit += value
                            total_debit = total_debit - value
                            continue
                        else:
                            total = total_debit + total_credit

                            if total > value:
                                cur.execute(
                                    'SELECT rate FROM PRINCIPAL WHERE debit = (?)', (value,))
                                rate = cur.fetchone()[0]

                                value_total = markup_debit_formula(
                                    rate, value)
                                total_markup_balance += value_total
                                total = total - value
                                continue
                            else:
                                cur.execute(
                                    'SELECT rate FROM PRINCIPAL WHERE debit = (?)', (value,))
                                rate = cur.fetchone()[0]

                                value_total = markup_debit_formula(
                                    rate, total)
                            total_markup_balance += value_total
            if balance == None:
                cur.execute(
                    'INSERT INTO MARKUP (date_id, debit) VALUES (?, ?)', (date_id, total_markup_balance,))
            else:
                cur.execute('UPDATE MARKUP SET debit = (?) WHERE date_id = (?)', (total_markup_balance, date_id,))

            if balance == (None,):
                cur.execute(
                    'SELECT debit FROM MARKUP WHERE id = (?)', (date_id,))
                debit = cur.fetchone()
                if debit == (None,):
                    pass
                else:
                    debit = debit[0]
                    total_balance += debit

                cur.execute(
                    'SELECT credit FROM MARKUP WHERE id = (?)', (date_id,))
                credit = cur.fetchone()
                if credit == (None,):
                    pass
                else:
                    credit = credit[0]
                    total_balance += credit

                cur.execute(
                    'UPDATE MARKUP SET balance = (?) WHERE id = (?)', (total_balance, date_id,))

        conn.commit()
        conn.close()


input_dates()
principal_calculations()
markup_calculations()
