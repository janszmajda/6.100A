# 6.100A Fall 2025
# Problem Set 1: Part B
# Name: <Jan Szmajda>
# Collaborators: <None>
# Time Spent: 4.5

############################################################
# Global variables
# Prior to running `test_ps1_student.py`, please comment
# these variables out!

# To be used for all three parts
# dates = "2024-08-01 2024-08-02 2024-08-03 2024-08-04 2024-08-05 \
#     2024-08-06 2024-08-07 2024-08-08 2024-08-09 2024-08-10"
# temperatures = "75.2 77.1 74.6 78.4 79.2 80.3 81.5 82.1 76.3 77.7"


# # To be used in third part
# target_temp = 78.0
# start_date = "2024-08-02"
# end_date = "2024-08-06"
############################################################


############################################################
# Complex String Processing
############################################################


# Task 1: Calculate the Average Temperature
# Your code here

temps = temperatures.split(" ")     #splitting the string list where the spaces occur
allAdded = 0

if len(temperatures) == 0:
    print(0)
else:
    for i in temps[0:len(temps)]:       #for loop to get the numerator for the average
        allAdded += float(i)
    avgTemp = allAdded / len(temps)     # average
    round(avgTemp, 2)
    print(f"Average temperature: {avgTemp}")

# Part 2: Calculate the Maximum and Minimum Temperatures
# Your code here

sortedTemps = sorted(temps)

maxTemp = sortedTemps[-1]
minTemp = sortedTemps[0]

print(f"\"Maximum temperature: {maxTemp}\"")
print(f"\"Minimum temperature: {minTemp}\"")


# Part 3: Finding the Closest Temperature (with a Guess-and-Check Approach)
# Your code here

datesArray = dates.split()
# temps = temps.split(" ")

sortedDates = sorted(datesArray)    # sorts the dates array we made from string of dates
# sortedTemps = sorted(temps)

if start_date < sortedDates[0]:     # if start date is less than first thing in sorted dates array
    start_date = sortedDates[0]     # then start date is rewritten as the first thing in sorted dates
if end_date > sortedDates[-1]:      # same for end dates but with last values
    end_date = sortedDates[-1]

differencesArray = []               # empty array that ill use to find smallest difference

for k in sortedTemps[0:len(sortedTemps)]:   # in sorted temps
    difference = target_temp - float(k)     # variable difference is the target temp minus the value of sorted temps
    differencesArray.append(abs(difference))    # after each iteration we add the difference to the differences Array

smallestDiff = min(differencesArray)     # made a variable to call the smallest value in differences array
smallestDiffIndex = differencesArray.index(smallestDiff)    # finding index of the smallest difference

# DEBUG STATEMENT print(sortedTemps[smallestDiffIndex]) # prints out the closest temp because the index of the smallestdiff matches a temperature in sorted temps

closestTemp = sortedTemps[smallestDiffIndex]  # defining value of closest temperature

tempIndex = temps.index(closestTemp)         # finding index of closest temperature on original temps array which corresponds to dates

print(f"\"Date with closest temperature: {datesArray[tempIndex]}\"") # prints dates that matches up with the index of the closest temperature


####################### -- Instructions I wrote for myself when doing this part -- #############################
# find closest temp in sortedTemps    GOT IT!!
# correspond that temp to a temp in temps and find its index     GOT IT!!
# correspond that index to the index of a date GOT IT!!
# print date GOT IT!!
