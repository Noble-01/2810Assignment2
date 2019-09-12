import sqlite3
import openpyxl
connection=sqlite3.connect('database.db')
cursor =connection.cursor()
from openpyxl import Workbook
wb = Workbook()
sheet =  wb.active
sheet.title = "Violations Types"
sheet["A1"] = 'Code'
sheet["B1"] = 'Description'
sheet["C1"] = 'Count'
sheet.column_dimensions['B'].width = 20

sql_command = """
select violation_code, violation_description, count(violation_code)
from violations
group by violation_code
"""
cursor.execute(sql_command)
result = cursor
for r in result:
    sheet.append(r)
counter = 0
for row in sheet.iter_rows(min_row=2):
    count = row[2].value
    counter +=count

lastRow = sheet.max_row
sheet['B'+str(lastRow +1 )] = 'Total violations'
sheet['C'+str(lastRow +1 )] = int(counter)
wb.save(filename = 'ViolationTypes.xlsx')
connection.commit()
connection.close()