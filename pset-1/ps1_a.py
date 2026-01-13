# 6.100A Fall 2025
# Problem Set 1: Part A
# Name: <Jan Szmajda>
# Collaborators: <None>
# Time Spent: <36 min>


############################################################
# Global variables
# Prior to running `test_ps1_student.py`, please comment
# these variables out!

# task_1_many_dates = "2024-08-01 2024-08-02 2024-08-03"
# task_2_date = "2024-08-01"
# task_3_date = "2024-08-02"
# task_4_date = "2024-08-03"
############################################################


############################################################
# Warm-up Tasks
############################################################


# Task 1: Finding the position of the first occurrence of a space
# Your code here
if task_1_many_dates.find(" ") == -1:
    print("Position of first space: None")
else:
    print(f"Position of first space: {task_1_many_dates.index(" ")}") #printing out the index of the first space character using the .index() command

# Task 2: Replacing dashes with slashes in a string
# Your code here

print(f"Modified string: {task_2_date.replace("-", "/")}") #used .replace("string", "string") to find and replace substring in string

# Task 3: Reversing the date into the opposite order
# Your code here
if len(task_3_date) == 0:
    print("Reversed string: None")
else:
    revstr = task_3_date[::-1]
    print("Reversed string:", revstr)

# Task 4: Date format conversion from YYYY-MM-DD to MM-DD-YYYY
# Your code here

if len(task_4_date) == 0:
    print("Converted date: None")
else:
    convstr = task_4_date[5:7] + "-" + task_4_date[8:10] + "-" + task_4_date[0:4]
    print(f"Converted date: {convstr}")
