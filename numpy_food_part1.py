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


sql_command = """
    SELECT facility_zip
    FROM inspections i LEFT JOIN violations v ON v.serial_number = i.serial_number 
    GROUP BY facility_zip 
    ORDER BY COUNT(v.violation_code) DESC;
"""
cursor.execute(sql_command)
postcodes = cursor.fetchall()
postCodeHigh = postcodes[0][0]
postCodeLow= postcodes[-1][0]

sql_command = """
SELECT COUNT(v.violation_code) 
FROM inspections i LEFT JOIN violations v ON v.serial_number = i.serial_number AND i.facility_zip = ? 
GROUP BY strftime("%Y-%m", i.activity_date) 
ORDER BY strftime("%Y-%m", i.activity_date)
"""
cursor.execute(sql_command,[postCodeHigh])
maxval = cursor.fetchall()

cursor.execute(sql_command,[postCodeLow])
lowval = cursor.fetchall()

sql_command ="""
    SELECT strftime("%Y-%m", i.activity_date), CAST(COUNT(v.violation_code) AS FLOAT)/CAST(COUNT(DISTINCT i.facility_zip) AS FLOAT) 
    FROM inspections i LEFT JOIN violations v ON v.serial_number = i.serial_number 
    GROUP BY strftime("%Y-%m", i.activity_date) 
    ORDER BY strftime("%Y-%m", i.activity_date);
"""
cursor.execute(sql_command)
avg = cursor.fetchall()

times =[]
maxVal = []
avgVal = []
minVal=[]


for i in range(len(avg)):
    times.append(avg[i][0])
    avgVal.append(avg[i][1])
    maxVal.append(maxval[i][0])
    minVal.append(lowval[i][0])
connection.close() 

plt.subplot(212)
plt.figure(figsize=(10,5))
plt.xticks(rotation=45)
plt.plot(times, avgVal, 'r-', times, maxVal, 'g-',times, minVal, 'c-')
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=3.0)
plt.show()

