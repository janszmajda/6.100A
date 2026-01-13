# 6.100A Fall 2025
# Problem Set 2: Part D
# Name: <Jan Szmajda>
# Collaborators: <None>
# Time Spent: 1 hour


############################################################
# Global variables
############################################################
# Bisection search_parameters
# Prior to running `test_ps2_student.py`, please comment
# these variables out!

# low = 50.0
# high = 100.0
# epsilon = 0.00001
# temperature = 82.0 # bisection search should output humidity of 85
# heat_threshold = 90.0
############################################################
# Constants for the heat index formula
# Be sure to leave these variables uncommented when running
# `test_ps2_student.py`!

c1 = -42.379
c2 = 2.04901523
c3 = 10.14333127
c4 = -0.22475541
c5 = -0.00683783
c6 = -0.05481717
c7 = 0.00122874
c8 = 0.00085282
c9 = -0.00000199
############################################################


############################################################
# Estimating the heat warning threshold using bisection search
############################################################
# Your code here
def normal_round(num):
    """ Cannot use python's round command as when it sees a .5 value it rounds
    to the nearest even int. This function round .5 up all the time
    """

    # find first digit after decimal and if it's 5 round it up
    num_string = str(num)
    decimal_index = num_string.find(".")

    if decimal_index != -1 and num_string[decimal_index + 1] == "5":
        num = int(num // 1) + 1
    else:
        num = round(num)

    return num

R = (high + low) / 2
guess = c1 + c2 * temperature + c3 * R + c4 * temperature * R + c5 * temperature**2 + c6 * R**2 + c7 * temperature**2 * R + c8 * temperature * R**2 + c9 * temperature**2 * R**2

while abs(guess - heat_threshold) >= epsilon:
    if guess > heat_threshold:
        high = R
    elif guess < heat_threshold:
        low = R
    R = (high + low) / 2
    guess = c1 + c2 * temperature + c3 * R + c4 * temperature * R + c5 * temperature**2 + c6 * R**2 + c7 * temperature**2 * R + c8 * temperature * R**2 + c9 * temperature**2 * R**2

print(f"Relative humidity threshold: {normal_round(R)}")
