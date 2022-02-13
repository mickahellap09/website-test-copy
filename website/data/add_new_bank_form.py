import PySimpleGUI as sg
import pandas as pd
import sqlite3
import create_all_dbs

conn_banks = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite', check_same_thread=False)
cur_banks = conn_banks.cursor()

# Add some color to the window
sg.theme('DarkTeal9')

layout = [
    [sg.Text('Please fill out the following fields:')],
    [sg.Text('Bank Name', size=(15, 1)), sg.InputText(key='bank_name')],
    [sg.Text('Bank Type', size=(15, 1)), sg.Checkbox(
        'Conventional', key='conventional'), sg.Checkbox('Islamic', key='islamic')],
    [sg.Text('Rate (leave blank for Islamic)', size=(15, 1)), sg.InputText(key='rate')],
    [sg.Text('Date DD/MM/YYYY', size=(15, 1)), sg.InputText(key='date')],
    [sg.Submit(), sg.Exit()]
]

window = sg.Window('Add New Bank Form', layout)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        try:
            conn.close()
        except:pass
        
        break
    if event == 'Submit':
        bank_name = values['bank_name']
        date = values['date']
        rate = values['rate']
        if values['conventional'] == True:
            bank_type = 'conventional'
        elif values['islamic'] == True:
            bank_type = 'islamic'
        else:
            break

        create_all_dbs.add_new_bank(bank_name, bank_type, date)

        if bank_type == 'conventional':
            
            conn = sqlite3.connect(
                f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite', check_same_thread=False)
            cur = conn.cursor() 

            cur.execute('SELECT id FROM dates WHERE dates.date = (?)', (date,))
            date_id = cur.fetchone()[0]

            cur.execute('INSERT INTO rates(rate, date_id) VALUES (?,?)', (rate, date_id,))

            conn.commit()