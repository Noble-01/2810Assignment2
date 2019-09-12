import sqlite3
import openpyxl

connection=sqlite3.connect('database.db')
cursor =connection.cursor()
sql_command = "drop table if exists violations ;"
cursor.execute(sql_command)
sql_command = "drop table if exists inspections ;"
cursor.execute(sql_command)
sql_command = """
create table violations(
point int,
serial_number text,
violation_code text,
violation_description text,
violation_status text
);
"""
cursor.execute(sql_command)
sql_command = """
create table inspections(
activity_date date ,
employee_id text ,
facility_address text ,
facility_city text ,
facility_id text ,
facility_name text ,
facility_state text ,
facility_zip text ,
grade text,
owner_id text,
owner_name text,
pe_description text,
program_element_pe int,
program_name text,
program_status text,
record_id text ,
score int,
serial_number text ,
service_code int,
service_description text 
);
"""
cursor.execute(sql_command)
connection.commit()
#sql = "PRAGMA table_info ('violations');"
#cursor.execute(sql)
#result = cursor.fetchall()
#print(result)

wb_violations = openpyxl.load_workbook('violations.xlsx')
wb_inspections = openpyxl.load_workbook('inspections.xlsx')
sheet_viol = wb_violations['violations']
sheet_inspec = wb_inspections['inspections']


viol_query = """ insert into violations (point, serial_number, violation_code, violation_description, violation_status) values (?,?,?,?,?)"""
inspec_query=""" insert into inspections values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
for row in sheet_viol.iter_rows(min_row=2):
    cursor.execute(viol_query,[row[i].value for i in range(5)])
for row in sheet_inspec.iter_rows(min_row=2):
    cursor.execute(inspec_query,[row[i].value for i in range(20)])
    
connection.commit()
connection.close()