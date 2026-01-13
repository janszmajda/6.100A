# 6.100A Fall 2025
# Problem Set 2: Part B
# Name: <Jan Szmajda>
# Collaborators: <None>
# Time Spent: 30min


############################################################
# Global variables
# Prior to running `test_ps2_student.py`, please comment
# these variables out!

# daily_forecast = "sunny cloudy rainy sunny sunny"
############################################################


############################################################
# Count each type of forecast
############################################################

# Your code here

daily_forecast_array = daily_forecast.split()
sunny_count = daily_forecast_array.count("sunny")
cloudy_count = daily_forecast_array.count("cloudy")
rainy_count = daily_forecast_array.count("rainy")
partly_cloudy_count = daily_forecast_array.count("partly_cloudy")

print(f"Sunny count: {sunny_count}")
print(f"Cloudy count: {cloudy_count}")
print(f"Rainy count: {rainy_count}")
print(f"Partly cloudy count: {partly_cloudy_count}")
