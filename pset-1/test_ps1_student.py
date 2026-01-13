import io
import os
import re
import sys
import unittest
from functools import wraps

# Get the directory of the current test script
current_directory = os.path.dirname(os.path.abspath(__file__))


def run_student_script(script_path, injected_globals):
    with open(script_path, "r") as f:
        student_code = f.read()

    # Capture output
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # collect a log of all printed lines to distinguish from stack traces
    printed_lines = []

    class PrintLog:
        def write(self, text):
            printed_lines.append(text)

    def log_print(*args, **kwargs):
        # this line redirects to printed_lines var
        print(*args, **kwargs, file=PrintLog())
        # this one goes to stddout
        print(*args, **kwargs)

    locals = {}
    try:
        end_state = exec(student_code, {**injected_globals, "print": log_print}, locals)
    except Exception as e:
        print(f"Error: {e}")

    sys.stdout = sys.__stdout__
    return (captured_output.getvalue().strip(), locals, printed_lines)


def case_options(points, failure, error):
    """Decorator to add points and messages to a test case"""

    def decorator(func):
        # Directly set attributes on the original function
        func.points = points
        func.failure_message = failure
        func.error_message = error

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


########### PART A ###########


class TestProblemSetBase(unittest.TestCase):
    """
    Base class for the test suite
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_script_path = None
        self.global_vars = {}

    def attempt_cases(self, inputs, expected):
        """Attempt the test cases for a given task"""

        injected_globals = self.global_vars.copy()
        injected_globals.update(inputs)

        output, _, _ = run_student_script(self.student_script_path, injected_globals)

        for expected_output in expected:
            if str(expected_output).lower() not in output.lower():
                self.fail(f"Expected {expected_output}, got {output}")

    def get_global_vars(self):
        return self.global_vars


class TestProblemSetPartA(TestProblemSetBase):
    """
    Test suite for Part A of Problem Set 1
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_script_path = os.path.join(current_directory, "ps1_a.py")

        self.global_vars = {
            "task_1_many_dates": "2024-08-01 2024-08-02 2024-08-03",
            "task_2_date": "2024-08-01",
            "task_3_date": "2024-08-02",
            "task_4_date": "2024-08-03",
        }

    @case_options(
        1,
        "Your code does not find the first space correctly",
        "Task find_first_space error",
    )
    def test_find_first_space_1(self):

        inputs = {"task_1_many_dates": "2024-08-01 2024-08-02 2024-08-03"}
        expected = ["Position of first space: 10"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code doesn't handle lack of spaces correctly",
        "Task find_first_space error",
    )
    def test_find_first_space_2(self):

        inputs = {"task_1_many_dates": "2024-08-01"}
        expected = ["Position of first space: None"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not find the first space correctly",
        "Task find_first_space error",
    )
    def test_find_first_space_3(self):
        inputs = {"task_1_many_dates": "   "}
        expected = ["Position of first space: 0"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code doesn't handle lack of spaces correctly",
        "Task find_first_space error",
    )
    def test_find_first_space_4(self):

        inputs = {"task_1_many_dates": "NoSpacesHere"}
        expected = ["Position of first space: None"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1, "Your code does not replace dashes correctly", "Task replace_dashes error"
    )
    def test_replace_dashes_1(self):
        inputs = {"task_2_date": "2024-08-01"}
        expected = ["Modified string: 2024/08/01"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1, "Your code does not replace dashes correctly", "Task replace_dashes error"
    )
    def test_replace_dashes_2(self):

        inputs = {"task_2_date": "2024/08/01/2024/08/02"}
        expected = ["Modified string: 2024/08/01/2024/08/02"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1, "Your code does not replace dashes correctly", "Task replace_dashes error"
    )
    def test_replace_dashes_3(self):

        inputs = {"task_2_date": "- - -"}
        expected = ["Modified string: / / /"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1, "Your code does not replace dashes correctly", "Task replace_dashes error"
    )
    def test_replace_dashes_4(self):
        inputs = {"task_2_date": "1234-5678-9012"}
        expected = ["Modified string: 1234/5678/9012"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1, "Your code does not reverse the date correctly", "Task reverse_date error"
    )
    def test_reverse_date_1(self):
        inputs = {"task_3_date": "2024-08-02"}
        expected = ["Reversed string: 20-80-4202"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not reverse the date correctly with an empty string",
        "Task reverse_date error",
    )
    def test_reverse_date_2(self):

        inputs = {"task_3_date": ""}
        expected = ["Reversed string: None"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1, "Your code does not reverse the date correctly", "Task reverse_date error"
    )
    def test_reverse_date_3(self):
        inputs = {"task_3_date": "A"}
        expected = ["Reversed string: A"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1, "Your code does not reverse the date correctly", "Task reverse_date error"
    )
    def test_reverse_date_4(self):

        inputs = {"task_3_date": "ReverseMe"}
        expected = ["Reversed string: eMesreveR"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not convert the date correctly", "Task convert_date error",
    )
    def test_date_format_conversion_1(self):

        inputs = {"task_4_date": "2024-08-03"}
        expected = ["Converted date: 08-03-2024"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not convert the date correctly", "Task convert_date error",
    )
    def test_date_format_conversion_2(self):

        inputs = {"task_4_date": "1999-12-31"}
        expected = ["Converted date: 12-31-1999"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not convert the date correctly", "Task convert_date error",
    )
    def test_date_format_conversion_3(self):

        inputs = {"task_4_date": "0000-01-01"}
        expected = ["Converted date: 01-01-0000"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not convert the date correctly with an empty string", "Task convert_date error",
    )
    def test_date_format_conversion_4(self):

        inputs = {"task_4_date": ""}
        expected = ["Converted date: None"]

        return self.attempt_cases(inputs, expected)


########### PART B ###########


class TestProblemSetPartB(TestProblemSetBase):
    """
    Test suite for Part B of Problem Set 1
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_script_path = os.path.join(current_directory, "ps1_b.py")

        self.global_vars = {
            "dates": "2024-08-01 2024-08-02 2024-08-03 2024-08-04 2024-08-05",
            "temperatures": "75.2 77.1 74.6 78.4 79.2",
            "start_date": "2024-08-01",
            "end_date": "2024-08-05",
            "target_temp": 78,
        }

    @case_options(
        1,
        "Your code does not calculate the average temperature correctly",
        "Task calculate_average_temperature error",
    )
    def test_calculate_average_temperature_1(self):

        inputs = {
            "dates": "2024-08-01 2024-08-02 2024-08-03 2024-08-04 2024-08-05",
            "temperatures": "75.2 77.1 74.6 78.4 79.2",
        }
        expected = ["Average temperature: 76.9"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not calculate the average temperature correctly",
        "Task calculate_average_temperature error",
    )
    def test_calculate_average_temperature_2(self):

        inputs = {
            "dates": "2024-08-01 2024-08-02 2024-08-03",
            "temperatures": "60.0 61.0 62.0",
        }
        expected = ["Average temperature: 61.0"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not calculate the average temperature correctly",
        "Task calculate_average_temperature error",
    )
    def test_calculate_average_temperature_3(self):
        inputs = {
            "dates": "2024-08-01 2024-08-02 2024-08-03",
            "temperatures": "100.0 200.0 300.0",
        }
        expected = ["Average temperature: 200.0"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not calculate the min/max temperatures correctly",
        "Task calculate_min_max_temperature error",
    )
    def test_calculate_min_max_temperature_1(self):
        inputs = {
            "dates": "2024-08-01 2024-08-02 2024-08-03",
            "temperatures": "75.2 77.1 74.6",
        }

        expected = ["Maximum temperature: 77.1", "Minimum temperature: 74.6"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not calculate the min/max temperatures correctly",
        "Task calculate_min_max_temperature error",
    )
    def test_calculate_min_max_temperature_2(self):
        inputs = {
            "dates": "2024-08-01 2024-08-02 2024-08-03",
            "temperatures": "60.0 61.0 62.0",
        }

        expected = ["Maximum temperature: 62.0", "Minimum temperature: 60.0"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not calculate the min/max temperatures correctly",
        "Task calculate_min_max_temperature error",
    )
    def test_calculate_min_max_temperature_3(self):
        inputs = {
            "dates": "2024-08-01 2024-08-02 2024-08-03",
            "temperatures": "100.0 200.0 300.0",
        }

        expected = ["Maximum temperature: 300.0", "Minimum temperature: 100.0"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not calculate the closest temperature correctly",
        "Task find_closest_temperature error",
    )
    def test_find_closest_temperature_1(self):
        inputs = {
            "dates": "2024-08-01 2024-08-02 2024-08-03 2024-08-04 2024-08-05",
            "temperatures": "75.2 77.1 74.6 78.4 79.2",
            "target_temp": 78.0,
            "start_date": "2024-08-02",
            "end_date": "2024-08-05",
        }

        expected = ["Date with closest temperature: 2024-08-04"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not calculate the closest temperature correctly",
        "Task find_closest_temperature error",
    )
    def test_find_closest_temperature_2(self):
        inputs = {
            "dates": "2024-08-01 2024-08-02",
            "temperatures": "60.0 61.0",
            "target_temp": 61.5,
            "start_date": "2024-08-01",
            "end_date": "2024-08-02",
        }

        expected = ["Date with closest temperature: 2024-08-02"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not calculate the closest temperature correctly",
        "Task find_closest_temperature error",
    )
    def test_find_closest_temperature_3(self):
        inputs = {
            "dates": "2024-08-01 2024-08-02",
            "temperatures": "100.0 200.0",
            "target_temp": 250.0,
            "start_date": "2024-08-01",
            "end_date": "2024-08-03",
        }

        expected = ["Date with closest temperature: 2024-08-02"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not calculate the closest temperature correctly",
        "Task find_closest_temperature error",
    )
    def test_find_closest_temperature_4(self):
        inputs = {
            "dates": "2024-08-01 2024-08-02 2024-08-03 2024-08-04 2024-08-05",
            "temperatures": "75.2 77.1 74.6 78.4 79.2",
            "target_temp": 78.0,
            "start_date": "2024-08-02",
            "end_date": "2024-08-05",
        }

        expected = ["Date with closest temperature: 2024-08-04"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not calculate the closest temperature correctly",
        "Task find_closest_temperature error",
    )
    def test_find_closest_temperature_5(self):
        inputs = {
            "dates": "2024-08-01 2024-08-02",
            "temperatures": "60.0 61.0",
            "target_temp": 61.5,
            "start_date": "2024-08-01",
            "end_date": "2024-08-02",
        }

        expected = ["Date with closest temperature: 2024-08-02"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not calculate the closest temperature correctly",
        "Task find_closest_temperature error",
    )
    def test_find_closest_temperature_6(self):
        inputs = {
            "dates": "2024-08-01 2024-08-02",
            "temperatures": "100.0 200.0",
            "target_temp": 250.0,
            "start_date": "2024-08-01",
            "end_date": "2024-08-03",
        }

        expected = ["Date with closest temperature: 2024-08-02"]

        return self.attempt_cases(inputs, expected)


class Results_600(unittest.TextTestResult):
    """
    Custom test result class to capture output and points
    """

    def __init__(self, *args, **kwargs):
        super(Results_600, self).__init__(*args, **kwargs)

        self.output = []

        self.points = 0
        self.max_points = 0

    def addSuccess(self, test):
        method = getattr(test, getattr(test, "_testMethodName"))
        func = method.__func__
        pts = getattr(func, "points", 0)

        self.points += pts
        self.max_points += pts

        return super().addSuccess(test)

    def addFailure(self, test, err):

        method = getattr(test, getattr(test, "_testMethodName"))
        func = method.__func__
        pts = getattr(func, "points", 0)

        failure_message = getattr(func, "failure_message", "")

        self.output.append(f"❌ [-{pts}] {failure_message}, {err[1]}\n")
        self.max_points += pts

        super(Results_600, self).addFailure(test, err)

    def addError(self, test, err):
        method = getattr(test, getattr(test, "_testMethodName"))
        func = method.__func__
        pts = getattr(func, "points", 0)

        error_message = getattr(func, "error_message", "")

        self.output.append(f"❌ [-{pts}] {error_message}, {err[1]}\n")
        self.max_points += pts

        super(Results_600, self).addError(test, err)

    def getOutput(self):
        """
        Return the captured output
        """
        if self.points > 0:
            self.output.append(
                f"\n✅ [+{self.points}] {self.points == self.max_points and 'All' or 'Other'} tests passed!\n"
            )

        return "\n".join(self.output)

    def getPoints(self):
        """
        Return the total points
        """

        return self.points


if __name__ == "__main__":

    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestProblemSetPartA))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestProblemSetPartB))

    runner = unittest.TextTestRunner(resultclass=Results_600, verbosity=2)
    result = runner.run(suite)

    output = result.getOutput()
    points_earned = round(result.getPoints(), 3)

    print(output)

    print(f"Total points: {points_earned} / {result.max_points}")
