import sqlite3
import xlsxwriter

conn_banks = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite')
cur_banks = conn_banks.cursor()

cur_banks.execute('SELECT name FROM BANKS')
all_banks = cur_banks.fetchall()

excel_path = 'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\reports\\bank_data.xlsx'
workbook = xlsxwriter.Workbook(excel_path)


def sheet_layout(sheet):
    bold = workbook.add_format({'bold': True})
    bold.set_align('center')

    sheet.merge_range('E1:H1', 'Principal', bold)
    sheet.merge_range('J1:L1', 'Markup', bold)
    sheet.write('B2', 'ID')
    sheet.write('C2', 'Date')
    sheet.write('E2', 'Rate')
    sheet.write('F2', 'Debit')
    sheet.write('G2', 'Credit')
    sheet.write('H2', 'Balance')
    sheet.write('J2', 'Debit')
    sheet.write('K2', 'Credit')
    sheet.write('L2', 'Balance')


for bank_name in all_banks:
    bank_name = bank_name[0]

    path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    filename = bank_name + '_bank_data.csv'

    worksheet = workbook.add_worksheet(bank_name)
    sheet_layout(worksheet)

    DATES = ['id', 'date']
    PRINCIPAL = ['rate', 'debit', 'credit', 'balance']
    MARKUP = ['debit', 'credit', 'balance']

    column_number = 1

    for column in DATES:
        sql_query = f'SELECT {column} FROM DATES'
        cur.execute(sql_query)
        all_values = cur.fetchall()
        row_number = 2

        for value in all_values:
            value = value[0]

            worksheet.write(row_number, column_number, value)
            row_number += 1
        column_number = column_number + 1
    column_number = column_number + 1

    for column in PRINCIPAL:
        sql_query = f'SELECT {column} FROM PRINCIPAL'
        cur.execute(sql_query)
        all_values = cur.fetchall()
        row_number = 2

        for value in all_values:
            value = value[0]
            worksheet.write(row_number, column_number, value)
            row_number += 1
        column_number = column_number + 1
    column_number = column_number + 1

    for column in MARKUP:
        sql_query = f'SELECT {column} FROM MARKUP'
        cur.execute(sql_query)
        all_values = cur.fetchall()
        row_number = 2

        for value in all_values:
            value = value[0]
            worksheet.write(row_number, column_number, value)
            row_number += 1
        column_number = column_number + 1

    conn.close()

workbook.close()
