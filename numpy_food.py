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
    SELECT strftime("%Y-%m", i.activity_date), CAST(COUNT(v.violation_code) AS FLOAT)/CAST(COUNT(DISTINCT v.serial_number ) AS FLOAT) 
    FROM inspections i LEFT JOIN violations v ON v.serial_number = i.serial_number
    WHERE i.program_name LIKE 'MCDONALDS'
    GROUP BY strftime("%Y-%m", i.activity_date) 
    ORDER BY strftime("%Y-%m", i.activity_date);
"""
cursor.execute(sql_command)
macAvg = cursor.fetchall()

sql_command ="""
    SELECT strftime("%Y-%m", i.activity_date), CAST(COUNT(v.violation_code) AS FLOAT)/CAST(COUNT(DISTINCT v.serial_number ) AS FLOAT) 
    FROM inspections i LEFT JOIN violations v ON v.serial_number = i.serial_number
    WHERE i.program_name LIKE 'BURGER KING'
    GROUP BY strftime("%Y-%m", i.activity_date) 
    ORDER BY strftime("%Y-%m", i.activity_date);
"""
cursor.execute(sql_command)
burAvg = cursor.fetchall()
sql_command ="""
    SELECT strftime("%Y-%m", i.activity_date), CAST(COUNT(v.violation_code) AS FLOAT)/CAST(COUNT(DISTINCT v.serial_number ) AS FLOAT), COUNT(DISTINCT v.serial_number ) 
    FROM inspections i LEFT JOIN violations v ON v.serial_number = i.serial_number
    WHERE i.program_name LIKE 'BURGER KING'
    GROUP BY strftime("%Y-%m", i.activity_date) 
    ORDER BY strftime("%Y-%m", i.activity_date);
"""
cursor.execute(sql_command)
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

