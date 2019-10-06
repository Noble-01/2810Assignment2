#import modules from sqlite3
import sqlite3
#opens the text file called 'sql_food.txt' with only writing privileges
#if the text file does not exist then it is created
#everytime this script runs the text file is emptied
f= open("sql_food.txt","w+")
# Connecting to the sqlite3 database called database.db
connection=sqlite3.connect('database.db')
cursor =connection.cursor()
#drops table 'Previous_Violations'if it exists already
sql_command = "drop table if exists Previous_Violations ;"
cursor.execute(sql_command)
sql_command = """
create table Previous_Violations(
facility_name text ,
facility_address text ,
facility_zip text ,
facility_city text 
);
"""
cursor.execute(sql_command)
#query used to insert values into the table by using a nested query that has a select statment
#within the insert statement
#select query only selects business that are distinct/different and have one violation at least
#results returned are ordered by their name in alphabetic order
database_query ="""
insert into Previous_Violations (facility_name,facility_address, facility_zip, facility_city)
select distinct I.facility_name,I.facility_address,I.facility_zip,I.facility_city
from violations V, inspections I
where  V.serial_number = I.serial_number
order by facility_name asc;
"""
cursor.execute(database_query)
#query is used to insert values into the text file
#query selects distinct businesses names and count of violation codes
#results returned are ordered by the highest to lowest number of violation codes
cursor.execute("""
select facility_name,count(violation_code) as totalViolations
from violations V, inspections I
where  V.serial_number = I.serial_number
group by i.facility_name, i.facility_address, i.facility_city, i.facility_zip
order by totalViolations desc;
""")
#store all the results retrieved into a variable
result = cursor.fetchall()
#run through the list stored in the variable and append it to the text file
for r in result:
    #after each insert of a business move to a new line
    f.write(str(r)+'\n')
#closes the opened file
f.close() 
# Saves and closes the connection for the database
connection.commit()
connection.close()
