import openpyxl
import sqlite3
import numpy as np

def readTable(filename):
	#load in excel file and make it active
	wb_obj = openpyxl.load_workbook(filename, data_only=True)
	sheet = wb_obj.active

	print(sheet.max_row)

	#delete rows that are empty at the end of the file
	rowIndex = 0
	for row in sheet.iter_rows():
		if row[0].value == None:
			sheet.delete_rows(rowIndex+2, sheet.max_row-1)
			break
		rowIndex+=1

	print(sheet.max_row)

	#instantiate variables and create 2D array (a)
	sheet_length = sheet.max_row
	columns = 10
	rows = sheet_length-4
	colIndex = 0
	rowIndex = 0
	a = [[0 for x in range(columns)] for y in range(rows)]
	b = [0 for x in range(4)]
	shiftValue = 'A'

	# rowIndex = 0
	#read through the file and store in table (a)
	for row in sheet.iter_rows(min_row=4, max_row=sheet_length-1):
		for cell in row:
			#adding an extra column that contains shift value (not in spreadsheet)
			if colIndex%columns == 1:
				colIndex+=1
			if cell.value != None:
				if 'Shift' in str(cell.value):
					shiftValue = str(cell.value)[-1]

				# print(rowIndex)
				a[rowIndex][1] = shiftValue
				a[rowIndex][colIndex%columns] = cell.value
			else:
				a[rowIndex][colIndex%columns] = "None"
			colIndex+=1
		rowIndex+=1

	#store all average values into b
	for i in range (3, 7):
		b[i-3] = str(sheet[sheet_length][i].value)

	a = np.array(a)
	b = np.array(b)

	print(a[0, :])

	return a, b

def addToDatabase(a):
	filepath = '/Users/balahaha/Desktop/website-test-copy-master/website/data/databases/'

	cane_sampling_connection = sqlite3.connect(filepath + 'cane_sampling.sqlite3', check_same_thread=False)
	cane_sampling_cursor = cane_sampling_connection.cursor()

	#create report table
	cane_sampling_cursor.executescript(
		'''CREATE TABLE IF NOT EXISTS REPORT_12_02_2022(sr INTEGER, shift TEXT, 'shift details' TEXT, token INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, brix REAL, pol REAL, pty REAL, rec REAL, rec_2 REAL, ded INTEGER);''')


	#store all values in a into the table
	cane_sampling_cursor.executemany('INSERT OR REPLACE INTO REPORT_12_02_2022 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', a);

	cane_sampling_connection.commit()
	cane_sampling_connection.close()

def averageTable(b):
	filepath = '/Users/balahaha/Desktop/website-test-copy-master/website/data/databases/'

	cane_sampling_connection = sqlite3.connect(filepath + 'cane_sampling.sqlite3', check_same_thread=False)
	cane_sampling_cursor = cane_sampling_connection.cursor()

	#create average table
	cane_sampling_cursor.executescript(
		'''CREATE TABLE IF NOT EXISTS AVERAGE_12_02_2022(brix REAL, pol REAL, pty REAL, rec REAL);''')

	#store values from b in average table
	cane_sampling_cursor.executemany('INSERT OR REPLACE INTO AVERAGE_12_02_2022 VALUES(?, ?, ?, ?);', [b]);

	cane_sampling_connection.commit()
	cane_sampling_connection.close()


if __name__ == '__main__':
	[a, b] = readTable('Excel_data/Cane Sampling 12-02-2022.xlsx')
	addToDatabase(a)
	averageTable(b)







