from unicodedata import name
import PySimpleGUI as sg
import sqlite3
import os
import update_databases

conn_banks = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite', check_same_thread=False)
cur_banks = conn_banks.cursor()

cur_banks.execute('SELECT name FROM banks')
bank_names = cur_banks.fetchall()

add_new_bank = 'Add New Bank'
bank_names.append(add_new_bank)

cur_banks.execute('SELECT id FROM bank_types WHERE bank_types.type = (?)', ('conventional',))
conventional_id = cur_banks.fetchone()[0]

# Add some color to the window
sg.theme('DarkTeal9')

layout = [
    [sg.Text('Please fill out the following fields:')],
    [sg.Text('Bank Name', size=(15, 1)),
     sg.Combo(bank_names, key='bank_name')],
    [sg.Text('Rate (leave blank for conventional)', size=(15, 1)), sg.InputText(key='rate')],
    [sg.Text('Amount', size=(15, 1)), sg.InputText(key='amount')],
    [sg.Text('Date DD/MM/YYYY', size=(15, 1)), sg.InputText(key='date')],
    [sg.Submit(), sg.Exit()]
]

window = sg.Window('Borrowing Form', layout)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        try:
            conn.close()
        except:pass
        break
    if event == 'Submit':
        bank_name = values['bank_name']
        if bank_name == 'Add New Bank':
            filepath = r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\add_new_bank_form.py'
            os.startfile(filepath)
            break

        else:
            date = values['date']
            amount = values['amount']
            rate = values['rate']
            transaction_type = 'principal'
            debit_or_credit = 'debit'
            bank_name = bank_name[0]
            cur_banks.execute('SELECT bank_type_id FROM banks WHERE banks.name = (?)', (bank_name,))
            bank_type_id = cur_banks.fetchone()[0]

            if bank_type_id == conventional_id:
                update_databases.add_new_transaction_debit_conventional(bank_name, transaction_type, debit_or_credit, amount, date)

                path = f'C:\\Users\\Taimur Adam\\Desktop\\test3\\data\\{bank_name}_bank_data.sqlite'
                conn = sqlite3.connect(path, check_same_thread=False)
                cur = conn.cursor()
                
                cur.execute('SELECT id FROM dates WHERE dates.date = (?)', (date,))
                date_id = cur.fetchone()[0]

                cur.execute('INSERT INTO rates(rate, date_id) VALUES (?, ?)', (rate, date_id,))

                conn.commit()

            else:
                update_databases.add_new_transaction_debit_islamic(bank_name, transaction_type, debit_or_credit, rate, amount, date)