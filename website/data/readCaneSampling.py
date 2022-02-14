import openpyxl
import sqlite3
import numpy as np
from os import listdir

def readTable(filename):
	#load in excel file and make it active
	wb_obj = openpyxl.load_workbook(filename, data_only=True)
	sheet = wb_obj.active

	# print(sheet.max_row)

	#delete rows that are empty at the end of the file
	rowIndex = 0
	for row in sheet.iter_rows():
		if row[0].value == None:
			sheet.delete_rows(rowIndex+2, sheet.max_row-1)
			break
		rowIndex+=1

	# print(sheet.max_row)

	#instantiate variables and create 2D array (a)
	sheet_length = sheet.max_row
	columns = 10
	rows = sheet_length-4
	colIndex = 0
	rowIndex = 0
	a = [[0 for x in range(columns)] for y in range(rows)]
	b = [0 for x in range(4)]
	shiftValue = 'A'

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

	return a, b

def addToDatabase(filepath, a, date):
	cane_sampling_connection = sqlite3.connect(filepath + 'cane_sampling.sqlite3', check_same_thread=False)
	cane_sampling_cursor = cane_sampling_connection.cursor()

	#create report table
	fullCreateString = f'''CREATE TABLE IF NOT EXISTS REPORT{date}(sr INTEGER, shift TEXT, 'shift details' TEXT, token INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, brix REAL, pol REAL, pty REAL, rec REAL, rec_2 REAL, ded INTEGER);'''
	cane_sampling_cursor.executescript(fullCreateString)


	#store all values in a into the table
	fullInsertString = f'INSERT OR REPLACE INTO REPORT{date} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
	cane_sampling_cursor.executemany(fullInsertString, a);

	cane_sampling_connection.commit()
	cane_sampling_connection.close()

def averageTable(filepath, b, date):
	cane_sampling_connection = sqlite3.connect(filepath + 'cane_sampling.sqlite3', check_same_thread=False)
	cane_sampling_cursor = cane_sampling_connection.cursor()

	#create average table
	fullCreateString = f'''CREATE TABLE IF NOT EXISTS AVERAGE{date}(brix REAL, pol REAL, pty REAL, rec REAL);'''
	cane_sampling_cursor.executescript(fullCreateString)

	#store values from b in average table
	fullInsertString = f'INSERT OR REPLACE INTO AVERAGE{date} VALUES(?, ?, ?, ?);'
	cane_sampling_cursor.executemany(fullInsertString, [b]);

	cane_sampling_connection.commit()
	cane_sampling_connection.close()


if __name__ == '__main__':
	userDirectory = '/Users/balahaha/Desktop/website-test-copy-master/website/data/databases/'
	directory = 'Excel_data/cane_sampling_lab/'

	#collecting all the cane sampling files
	allFiles = listdir(directory)
	allFiles = allFiles[1:]

	#go through all cane sampling files and perform functionality
	for file in allFiles:
		filename = directory + file
		[a, b] = readTable(filename)
		date = "_" + filename[-15:-13] + "_" + filename[-12:-10] + "_" + filename[-9:-5]
		addToDatabase(userDirectory, a, date)
		averageTable(userDirectory, b, date)

