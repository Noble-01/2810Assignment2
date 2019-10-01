#----------------------------------------
#Use MatPlotLib to create a plot with the following data:
#    The number of violations per month for the postcode with the highest total
#    violations
#
#    The number of violations per month for the postcode with the lowest total
#    violations
#
#    The average number of violations per month for ALL of California (ALL
#    postcodes combined and averaged). For example, If postcode 1111 has 5
#    violations during July, 2222 has 4 violations during July, and 3333 has 3
#    violations for July, then the average violations in July is 4 (12 violations/3
#    postcodes)
#----------------------------------------

import matplotlib.pyplot as plt
import sqlite3
connection=sqlite3.connect('database.db')
cursor =connection.cursor()

sql_command ="""
    SELECT strftime("%Y-%m", i.activity_date), CAST(COUNT(v.violation_code) AS FLOAT)/(select count(distinct n.facility_name)  from inspections n where n.facility_name LIKE ?) 
    FROM inspections i LEFT JOIN violations v ON v.serial_number = i.serial_number and i.facility_name LIKE ?
    GROUP BY strftime("%Y-%m", i.activity_date) 
    ORDER BY strftime("%Y-%m", i.activity_date);
"""
cursor.execute(sql_command, ["%MCDONALD'S%","%MCDONALD'S%"])
macAvg = cursor.fetchall()

cursor.execute(sql_command, ["%BURGER KING%","%BURGER KING%"])
burAvg = cursor.fetchall()

result = cursor.fetchall()
for r in result: print(r)

times =[]
macAvgVal =[]
burgAvgVal = []

for i in range(len(burAvg)):
    times.append(macAvg[i][0])
    macAvgVal.append(macAvg[i][1])
    burgAvgVal.append(burAvg[i][1])
connection.close() 

plt.figure(figsize=(10,5))
plt.xticks(rotation=45)
plt.plot(times, macAvgVal, 'r-',times, burgAvgVal, 'b-')
plt.show()

