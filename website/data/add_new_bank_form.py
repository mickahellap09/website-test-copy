import PySimpleGUI as sg
import pandas as pd
import sqlite3
import create_all_dbs

conn_banks = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite')
cur_banks = conn_banks.cursor()

# Add some color to the window
sg.theme('DarkTeal9')

layout = [
    [sg.Text('Please fill out the following fields:')],
    [sg.Text('Bank Name', size=(15, 1)), sg.InputText(key='bank_name')],
    [sg.Text('Rate', size=(15, 1)), sg.InputText(key='rate')],
    [sg.Text('Date DD/MM/YYYY', size=(15, 1)), sg.InputText(key='date')],
    [sg.Submit(), sg.Exit()]
]

window = sg.Window('Add New Bank Form', layout)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Submit':
        name_of_bank = values['bank_name']
        date = values['date']
        rate = values['rate']

        create_all_dbs.add_new_bank(name_of_bank, rate, date)
