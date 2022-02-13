import sqlite3
from sqlalchemy import column
import xlsxwriter

conn_banks = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite', check_same_thread=False)
cur_banks = conn_banks.cursor()

cur_banks.execute('SELECT name FROM banks')
all_banks = cur_banks.fetchall()

excel_path = r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\reports\bank_data.xlsx'
workbook = xlsxwriter.Workbook(excel_path)


def sheet_layout(sheet):

    bold = workbook.add_format({'bold': True})
    bold.set_align('center')

    sheet.merge_range('E1:G1', 'Principal', bold)
    sheet.merge_range('I1:K1', 'Markup', bold)
    sheet.write('B2', 'ID')
    sheet.write('C2', 'Date')
    sheet.write('M2', 'Rate')
    sheet.write('E2', 'Debit')
    sheet.write('F2', 'Credit')
    sheet.write('G2', 'Balance')
    sheet.write('I2', 'Debit')
    sheet.write('J2', 'Credit')
    sheet.write('K2', 'Balance')

def update_sheets():
    for bank_name in all_banks:
        bank_name = bank_name[0]

        path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{bank_name}_bank_data.sqlite'
        conn = sqlite3.connect(path, check_same_thread=False)
        cur = conn.cursor()

        cur_banks.execute('SELECT id FROM bank_types WHERE bank_types.type = (?)', ('conventional',))
        conventional_id = cur_banks.fetchone()[0]

        cur_banks.execute('SELECT bank_type_id FROM banks WHERE banks.name = (?)', (bank_name,))
        bank_type_id = cur_banks.fetchone()[0]
        
        cur.execute('SELECT id FROM dates')
        all_date_ids = cur.fetchall()
        worksheet = workbook.add_worksheet(bank_name)
        sheet_layout(worksheet)


        dates = ['id', 'date']
        principal = ['principal_debit', 'principal_credit', 'principal_balance']
        markup = ['markup_debit', 'markup_credit', 'markup_balance']

        column_number = 1

        for column in dates:
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

        for column in principal:
            sql_query = f'SELECT {column} FROM view'
            cur.execute(sql_query)
            all_values = cur.fetchall()
            row_number = 2

            for value in all_values:
                value = value[0]
                worksheet.write(row_number, column_number, value)
                row_number += 1
            column_number = column_number + 1
        column_number = column_number + 1

        for column in markup:
            sql_query = f'SELECT {column} FROM view'
            cur.execute(sql_query)
            all_values = cur.fetchall()
            row_number = 2

            for value in all_values:
                value = value[0]
                worksheet.write(row_number, column_number, value)
                row_number += 1
            column_number = column_number + 1
        column_number = column_number + 1
        
        if bank_type_id == conventional_id:
            sql_query = f'SELECT rate, date_id FROM rates'
        else:
            sql_query = f'SELECT rate, date_id FROM transactions'
            cur.execute(sql_query)
            all_values = cur.fetchall()
            row_number = 2
            
            for value in all_values:
                value1 = value[1] + 1
                worksheet.write(value1,column_number, value[0])
                    

        conn.close()
    workbook.close()
    
update_sheets()