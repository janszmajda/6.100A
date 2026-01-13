# 6.100A Fall 2025
# Problem Set 2: Part A
# Name: <Jan Szmajda>
# Collaborators: <None>
# Time Spent: 3hrs


############################################################
# Global variables
# Prior to running `test_ps2_student.py`, please comment
# these variables out!

# temps = "75.2 77.1 75.2 78.4 79.2 75.2 81.5 82.1 77.1 77.1"
# min_temp = 75
# max_temp = 82
############################################################


############################################################
# Determining the mode with custom temperature binning
############################################################

############-- Make a function for standard rounding --#############

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

############-- Find most occurring temp --#############

temp_array = temps.split(" ")

rounded_numbers_string = ""
for i in temp_array:
    rounded_numbers_string += " " + str(normal_round(float(i)))
rounded_numbers_string = rounded_numbers_string.strip()     #remove a leading & trailing whitespace

rounded_temp_array = rounded_numbers_string.split()
rounded_temp_array = sorted(rounded_temp_array)

# making rounded temp array into int array
temperatures = []
for k in rounded_temp_array:
    temperatures.append(int(k))

# have sorted list of rounded int temps -- use max with a key for count
mode = max(temperatures[::-1], key=temperatures.count)
count = temperatures.count(mode)

print(f"Mode bin rounded temperature: {mode}")
print(f"Count: {count}")
