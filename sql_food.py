import sqlite3
connection=sqlite3.connect('database.db')
cursor =connection.cursor()
sql_command = "drop table if exists previousViolations ;"
cursor.execute(sql_command)
sql_command = """
create table previousViolations(
facility_name text ,
facility_address text ,
facility_zip text ,
facility_city text 
);
"""
cursor.execute(sql_command)
bus_query ="""
insert into previousViolations (facility_name,facility_address, facility_zip, facility_city)
select I.facility_name,I.facility_address,I.facility_zip,I.facility_city
from violations V, inspections I
where  V.serial_number = I.serial_number
group by facility_name
"""
cursor.execute(bus_query)
cursor.execute("""
select facility_name,count(violation_code) as totalViolations
from violations V, inspections I
where  V.serial_number = I.serial_number
group by facility_name
order by totalViolations desc
""")
result = cursor.fetchall()
for r in result:
    print(r)
connection.commit()
connection.close()