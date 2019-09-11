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
activity_date date not null,
employee_id varchar(12) not null,
facility_address varchar(120) not null,
facility_city varchar(60) not null,
facility_id varchar(12) not null,
facility_name varchar(100) not null,
facility_state varchar(2) not null,
facility_zip varchar(10) not null,
grade text(1) not null,
owner_id varchar(12) not null,
owner_name varchar(100) not null,
pe_description text(200) not null,
program_element_pe integer(4) not null,
program_name varchar(100) not null,
program_status text not null,
record_id varchar(12) not null,
score integer(3) not null,
serial_number varchar(15) not null,
service_description text(100) not null
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
inspec_query=""" insert into violation values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
for row in sheet_viol.iter_rows(min_row=2, max_row=20):
    cursor.execute(viol_query,[row[i].value for i in range(5)])
for row in sheet_inspec.iter_rows(min_row=2, max_row=20):
    cursor.execute(inspec_query,[row[i].value for i in range(20)])
    #values = (row[0].value,row[1].value, row[2].value, row[3].value, row[4].value)
    #print(point)  
    #cursor.execute(query,values)
    
connection.commit()
connection.close()