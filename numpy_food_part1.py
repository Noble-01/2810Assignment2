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
import matplotlib.patches as mpatches
import sqlite3
connection=sqlite3.connect('database.db')
cursor =connection.cursor()


sql_command = """
    SELECT facility_zip
    FROM inspections i, violations v
    WHERE v.serial_number = i.serial_number 
    GROUP BY facility_zip
    HAVING COUNT(v.violation_code)>=1
    ORDER BY COUNT(v.violation_code) DESC;
"""
cursor.execute(sql_command)
postcodes = cursor.fetchall()
postCodeHigh = postcodes[0][0]
postCodeLow= postcodes[-1][0]

sql_command = """
SELECT strftime("%Y-%m", i.activity_date),COUNT(v.violation_code) 
FROM inspections i LEFT JOIN violations v ON v.serial_number = i.serial_number AND i.facility_zip = ? 
GROUP BY strftime("%Y-%m", i.activity_date) 
ORDER BY strftime("%Y-%m", i.activity_date)
"""
cursor.execute(sql_command,[postCodeHigh])
maxval = cursor.fetchall()

cursor.execute(sql_command,[postCodeLow])
lowval = cursor.fetchall()
minValSingleViolation = []
minValSingleViolationTime=[]
for i in lowval:
    if i[1] == 1:
        minValSingleViolation.append(i[1])
        minValSingleViolationTime.append(i[0])
print(minValSingleViolation)
sql_command ="""
    SELECT CAST(COUNT(v.violation_code) AS FLOAT)/CAST(COUNT(DISTINCT i.facility_zip) AS FLOAT) 
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
    times.append(maxval[i][0])
    avgVal.append(avg[i][0])
    maxVal.append(maxval[i][1])
    minVal.append(lowval[i][1])


sql_command ="""
    SELECT strftime("%Y-%m", i.activity_date), CAST(COUNT(v.violation_code) AS FLOAT)/(select count(distinct n.facility_name)  from inspections n where n.facility_name LIKE ?) 
    FROM inspections i,violations v ON v.serial_number = i.serial_number and i.facility_name LIKE ?
    GROUP BY strftime("%Y-%m", i.activity_date) 
    ORDER BY strftime("%Y-%m", i.activity_date);
"""
cursor.execute(sql_command, ["%MCDONALD%","%MCDONALD%"])
macAvg = cursor.fetchall()

cursor.execute(sql_command, ["%BURGER KING%","%BURGER KING%"])
burAvg = cursor.fetchall()


times =[]
McDonaldsAvg =[]
BurgerKingAvg = []

for i in range(len(burAvg)):
    times.append(macAvg[i][0])
    McDonaldsAvg .append(macAvg[i][1])
    BurgerKingAvg.append(burAvg[i][1])
connection.close() 



plt.figure(figsize=(10,5))
plt.xticks(rotation=45)
plt.plot(times, avgVal, 'r-', times, maxVal, 'g-',times, minVal, 'c-', minValSingleViolationTime, minValSingleViolation, 'r*')
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=3.0)
ax = plt.axes()        
ax.yaxis.grid()
plt.ylabel("Number of violations")
plt.xlabel("Months")
plt.title("Number of violations for the postcode with highest,toal and average total of violation")
Max_Legend = mpatches.Patch(color='green', label='Maximum')
Avg_Legend = mpatches.Patch(color='red', label='Average')
Min_Legend = mpatches.Patch(color='blue', label='Minimum')
plt.legend(handles=[Max_Legend, Min_Legend, Avg_Legend])


plt.figure(figsize=(10,5))
plt.xticks(rotation=45)
plt.plot(times, McDonaldsAvg, 'r-',times, BurgerKingAvg, 'b-')
ax = plt.axes()        
ax.yaxis.grid()
plt.ylabel("Number of violations")
plt.xlabel("Months")
plt.title("Average number of violations per month (violations per month/total restaurants)")
McDonalds_Legend = mpatches.Patch(color='red', label='McDonalds')
Burger_King_legend = mpatches.Patch(color='blue', label='Burger King')
plt.legend(handles=[McDonalds_Legend,Burger_King_legend])

plt.show()


