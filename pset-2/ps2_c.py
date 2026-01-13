# 6.100A Fall 2025
# Problem Set 2: Part C
# Name: <Jan Szmajda>
# Collaborators: <None>
# Time Spent: 45min


############################################################
# Global variables
# Prior to running `test_ps2_student.py`, please comment
# these variables out!

# daily_forecast = "sunny cloudy sunny sunny sunny"
############################################################


############################################################
# Find the longest continuous sunny streak
############################################################

# Your code here

daily_forecast_array = daily_forecast.split()

current_streak = 0
longest_streak = 0

for i in daily_forecast_array:
    if i == "sunny":
        current_streak += 1
        if current_streak > longest_streak:
            longest_streak = current_streak
    else:
        current_streak = 0

print(f"Longest continuous sunny streak: {longest_streak}")
