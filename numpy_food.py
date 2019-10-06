#import modules from matplotlab
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
#import modules from sqlite 3
import sqlite3
# Connecting to the sqlite3 database called database.db
connection=sqlite3.connect('database.db')
cursor =connection.cursor()

#part 1
#query returns a list of postcodes that at least one violation
#results returned are ordered by the number of violation codes
#highest to lowest violation code
sql_command = """
    SELECT facility_zip
    FROM inspections i, violations v
    WHERE v.serial_number = i.serial_number 
    GROUP BY facility_zip
    HAVING COUNT(v.violation_code)>=1
    ORDER BY COUNT(v.violation_code) DESC;
"""
cursor.execute(sql_command)
#store all the results retrieved into a variable
postcodes = cursor.fetchall()
#assert the highest post code which will be at the top of the list to the variable postCodeHigh
postCodeHigh = postcodes[0][0]
#assert the lowest post code which will be at the bottom of the list to the variable postCodeLow
postCodeLow= postcodes[-1][0]

#query will return the number of violation codes per month for both lowest and highest post code.
#results returned are grouped and ordered by the month and year of the inspection
#the ? is used as a place holder to insert the value for the postcodes
#this saves having to write two queries for both postcodes
sql_command = """
SELECT strftime("%Y-%m", i.activity_date),COUNT(v.violation_code) 
FROM inspections i LEFT JOIN violations v ON v.serial_number = i.serial_number AND i.facility_zip = ? 
GROUP BY strftime("%Y-%m", i.activity_date) 
ORDER BY strftime("%Y-%m", i.activity_date)
"""
#execute the query with the value for highest postcode in the placholder
cursor.execute(sql_command,[postCodeHigh])
#store all the results retrieved into a variable
maxval = cursor.fetchall()

cursor.execute(sql_command,[postCodeLow])
lowval = cursor.fetchall()

#lists used to display a marker over the single violation for the lowest postcode
#this is done as it is impossible to notice any small raises in the line graph due to how large the y axis is
minValSmallViolation = []
minValSmallViolationTime=[]
#run through the values for the lowest postcode, if any value is in between 20 and 1 then add the time and value to the list
for i in lowval:
    #the range 20 to 1 was chosen as anything above 20 can be seen without struggle on the linegraph
    if i[1] >= 1 and i[1]<=20:
        minValSmallViolation.append(i[1])
        minValSmallViolationTime.append(i[0])

#query is used to select the average number of violations per month for all of California postcodes
sql_command ="""
    SELECT strftime("%Y-%m", i.activity_date), CAST(COUNT(v.violation_code) AS FLOAT)/CAST(COUNT(DISTINCT i.facility_zip) AS FLOAT) 
    FROM inspections i LEFT JOIN violations v ON v.serial_number = i.serial_number 
    GROUP BY strftime("%Y-%m", i.activity_date) 
    ORDER BY strftime("%Y-%m", i.activity_date);
"""
cursor.execute(sql_command)
avg = cursor.fetchall()

#lists to store the values retrieved from the queries above
maxVal = []
avgVal = []
minVal=[]

#run a for loop to append all the results fetched from the queries and stored in the variables to the lists
for i in range(len(avg)):
    avgVal.append(avg[i][1])
    maxVal.append(maxval[i][1])
    minVal.append(lowval[i][1])

#Part 2
#query is used to return the average number of violations per month for all McDonalds compared with the average number of violations for all Burger Kings
#the ? is used as a place holder to insert the name for the facilities
#this saves having to write two queries for both names
sql_command ="""
    SELECT strftime("%Y-%m", i.activity_date), CAST(COUNT(v.violation_code) AS FLOAT)/(select count(distinct n.facility_name)  from inspections n where n.facility_name LIKE ?) 
    FROM inspections i,violations v ON v.serial_number = i.serial_number and i.facility_name LIKE ?
    GROUP BY strftime("%Y-%m", i.activity_date) 
    ORDER BY strftime("%Y-%m", i.activity_date);
"""
#execute the query with the value for facility name in the placholder
cursor.execute(sql_command, ["%MCDONALD%","%MCDONALD%"])
macAvg = cursor.fetchall()

cursor.execute(sql_command, ["%BURGER KING%","%BURGER KING%"])
burAvg = cursor.fetchall()

#lists to store the values retrieved from the queries above
times =[]
McDonaldsAvg =[]
BurgerKingAvg = []
#run a for loop to append all the results fetched from the queries and stored in the variables to the lists
for i in range(len(burAvg)):
    times.append(macAvg[i][0])
    McDonaldsAvg .append(macAvg[i][1])
    BurgerKingAvg.append(burAvg[i][1])
#the two lists below are used to store x and y values for the large peaks in the graph
#these values will be used to place markers on the peaks to be used in the report
spikeTime = ['2015-10','2016-01','2016-03','2016-08','2016-09','2017-06','2017-10']
spikeGraph = [527,584,129,85,517,684,534]

#display the The number of violations per month for the postcode with the highest/lowest and average total violations
#display part 1
#change the size of the x axis figures and rotate them to 45 degrees so that they all fit on the screen
plt.figure(figsize=(10,5))
plt.xticks(rotation=45)
#plot the x,y coordinates for all three line graphs
#plot the markers for the line graphs (minValSmallViolationTime, minValSmallViolation,spikeTime,spikeGraph)
plt.plot(times, avgVal, 'r-', times, maxVal, 'g-',times, minVal, 'b-', minValSmallViolationTime, minValSmallViolation, 'r*', spikeTime,spikeGraph,'b*')
#create y grid lines
ax = plt.axes()        
ax.yaxis.grid()
#create a x and y axis label
plt.ylabel("Number of violations")
plt.xlabel("Months")
#create a title for the line graph
plt.title("Number of violations for the postcode with highest, lowest and average total of violation")
#create a legend that displays the names for the different line graphs
Max_Legend = mpatches.Patch(color='green', label='Maximum')
Avg_Legend = mpatches.Patch(color='red', label='Average')
Min_Legend = mpatches.Patch(color='blue', label='Minimum')
plt.legend(handles=[Max_Legend, Min_Legend, Avg_Legend])

#display the average number of violations per month for all McDonalds compared with the average number of violations for all Burger Kings
#display part 2
#the code below is the same as the display above with different coordinates plotted
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
#show the graphs
plt.show()
# Saves and closes the connection for the database
connection.commit()
connection.close()
