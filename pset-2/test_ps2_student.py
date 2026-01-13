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

    printed_lines = [line for line in printed_lines if line.strip()]

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


class TestProblemSetBase(unittest.TestCase):
    """
    Base class for the test suite
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_script_path = None
        self.global_vars = {}

    def attempt_cases(self, inputs, expected, exact_match=False, exact_lines=False):
        """Attempt the test cases for a given task"""

        injected_globals = self.global_vars.copy()
        injected_globals.update(inputs)

        output, _, printed_lines = run_student_script(
            self.student_script_path, injected_globals
        )

        # lists of expected outputs
        if isinstance(expected, list):
            for expected_output in expected:
                if exact_match and expected_output != output:
                    self.fail(f"Expected {expected_output}, got {output}")
                elif (
                    not exact_match
                    and str(expected_output).lower() not in output.lower()
                ):
                    self.fail(f"Expected {expected_output}, got {output}")

        # tuple of expected outputs, in exact order
        elif isinstance(expected, tuple):

            if exact_lines and len(expected) != len(printed_lines):
                self.fail(f"Expected {len(expected)} outputs, got {len(printed_lines)}")

            for i, expected_output in enumerate(expected):
                if exact_match and expected_output != printed_lines[i]:
                    self.fail(f"Expected {expected_output}, got {printed_lines[i]}")
                elif (
                    not exact_match
                    and str(expected_output).lower() not in printed_lines[i].lower()
                ):
                    self.fail(f"Expected {expected_output}, got {printed_lines[i]}")

    def get_global_vars(self):
        return self.global_vars


# ########### PART A ###########
class TestProblemSetPartA(TestProblemSetBase):
    """
    Test suite for Part A of Problem Set 2
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_script_path = os.path.join(current_directory, "ps2_a.py")

        self.global_vars = {
            "temps": "75.2 77.1 75.2 78.4 79.2 75.2 81.5 81.9 77.1 77.1",
            "min_temp": 75,
            "max_temp": 82,
        }

    @case_options(
        1,
        "Your code does not find the mode bin and count correctly",
        "Task find_mode_bin_and_count error",
    )
    def test_find_mode_bin_and_count_1(self):

        inputs = {
            "temps": "75.2 77.1 75.2 78.4 79.2 75.2 81.5 81.9 77.1 77.1",
            "min_temp": 75,
            "max_temp": 82,
        }
        expected = ("Mode bin rounded temperature: 77", "Count: 3")

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not find the mode bin and count correctly",
        "Task find_mode_bin_and_count error",
    )
    def test_find_mode_bin_and_count_2(self):

        inputs = {
            "temps": "77.0 76.8 81.0",
            "min_temp": 75,
            "max_temp": 82,
        }
        expected = ("Mode bin rounded temperature: 77", "Count: 2")

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not find the mode bin and count correctly",
        "Task find_mode_bin_and_count error",
    )
    def test_find_mode_bin_and_count_3(self):

        inputs = {
            "temps": "85.0 85.4 80.0",
            "min_temp": 78,
            "max_temp": 86,
        }
        expected = ("Mode bin rounded temperature: 85", "Count: 2")

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not find the mode bin and count correctly",
        "Task find_mode_bin_and_count error",
    )
    def test_find_mode_bin_and_count_4(self):

        inputs = {
            "temps": "78.4 77.6 80.5 81.2",
            "min_temp": 75,
            "max_temp": 82,
        }
        expected = ("Mode bin rounded temperature: 81", "Count: 2")

        return self.attempt_cases(inputs, expected)


########### PART B ###########
class TestProblemSetPartB(TestProblemSetBase):
    """
    Test suite for Part B of Problem Set 2
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_script_path = os.path.join(current_directory, "ps2_b.py")

        self.global_vars = {
            "daily_forecast": "sunny cloudy rainy sunny sunny",
        }

    @case_options(
        1,
        "Your code does not count each type of forecast correctly",
        "Task count_each_type_of_forecast error",
    )
    def test_count_each_type_of_forecast_1(self):

        inputs = {
            "daily_forecast": "sunny cloudy rainy sunny sunny",
        }
        expected = (
            "Sunny count: 3",
            "Cloudy count: 1",
            "Rainy count: 1",
            "Partly cloudy count: 0",
        )

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not count each type of forecast correctly",
        "Task count_each_type_of_forecast error",
    )
    def test_count_each_type_of_forecast_2(self):

        inputs = {
            "daily_forecast": "sunny sunny sunny sunny sunny",
        }
        expected = (
            "Sunny count: 5",
            "Cloudy count: 0",
            "Rainy count: 0",
            "Partly cloudy count: 0",
        )

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not count each type of forecast correctly",
        "Task count_each_type_of_forecast error",
    )
    def test_count_each_type_of_forecast_3(self):

        inputs = {
            "daily_forecast": "cloudy cloudy cloudy",
        }
        expected = (
            "Sunny count: 0",
            "Cloudy count: 3",
            "Rainy count: 0",
            "Partly cloudy count: 0",
        )

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not count each type of forecast correctly",
        "Task count_each_type_of_forecast error",
    )
    def test_count_each_type_of_forecast_4(self):

        inputs = {
            "daily_forecast": "rainy partly_cloudy sunny",
        }
        expected = (
            "Sunny count: 1",
            "Cloudy count: 0",
            "Rainy count: 1",
            "Partly cloudy count: 1",
        )

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not count each type of forecast correctly",
        "Task count_each_type_of_forecast error",
    )
    def test_count_each_type_of_forecast_5(self):

        inputs = {
            "daily_forecast": "",
        }
        expected = (
            "Sunny count: 0",
            "Cloudy count: 0",
            "Rainy count: 0",
            "Partly cloudy count: 0",
        )

        return self.attempt_cases(inputs, expected)


########### PART C ###########
class TestProblemSetPartC(TestProblemSetBase):
    """
    Test suite for Part C of Problem Set 2
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_script_path = os.path.join(current_directory, "ps2_c.py")

        self.global_vars = {
            "daily_forecast": "sunny cloudy sunny sunny sunny",
        }

    @case_options(
        1,
        "Your code does not find the longest continuous sunny day streak correctly",
        "Task find_longest_continuous_sunny_day_streak error",
    )
    def test_find_longest_continuous_sunny_day_streak_1(self):

        inputs = {
            "daily_forecast": "sunny sunny sunny cloudy sunny",
        }
        expected = ("Longest continuous sunny streak: 3",)

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not find the longest continuous sunny day streak correctly",
        "Task find_longest_continuous_sunny_day_streak error",
    )
    def test_find_longest_continuous_sunny_day_streak_2(self):

        inputs = {
            "daily_forecast": "sunny sunny sunny sunny sunny",
        }
        expected = ("Longest continuous sunny streak: 5",)

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not find the longest continuous sunny day streak correctly",
        "Task find_longest_continuous_sunny_day_streak error",
    )
    def test_find_longest_continuous_sunny_day_streak_3(self):

        inputs = {
            "daily_forecast": "cloudy cloudy cloudy",
        }
        expected = ("Longest continuous sunny streak: 0",)

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not find the longest continuous sunny day streak correctly",
        "Task find_longest_continuous_sunny_day_streak error",
    )
    def test_find_longest_continuous_sunny_day_streak_4(self):

        inputs = {
            "daily_forecast": "rainy partly_cloudy sunny",
        }
        expected = ("Longest continuous sunny streak: 1",)

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not find the longest continuous sunny day streak correctly",
        "Task find_longest_continuous_sunny_day_streak error",
    )
    def test_find_longest_continuous_sunny_day_streak_5(self):

        inputs = {
            "daily_forecast": "",
        }
        expected = ("Longest continuous sunny streak: 0",)

        return self.attempt_cases(inputs, expected)


########### PART D ###########
class TestProblemSetPartD(TestProblemSetBase):
    """
    Test suite for Part D of Problem Set 2
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_script_path = os.path.join(current_directory, "ps2_d.py")

        self.global_vars = {
            "low": 0.0,
            "high": 100.0,
            "epsilon": 0.00001,
            "temperature": 35.0,
            "heat_threshold": 40.0,
        }

    @case_options(
        1,
        "Your code does not find the relative humidity threshold correctly",
        "Task find_relative_humidity_threshold error",
    )
    def test_find_relative_humidity_threshold_1(self):

        inputs = {
            "low": 50.0,
            "high": 100.0,
            "epsilon": 0.00001,
            "temperature": 83.8,
            "heat_threshold": 90.0,
        }
        expected = ["Relative humidity threshold: 70"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not find the relative humidity threshold correctly",
        "Task find_relative_humidity_threshold error",
    )
    def test_find_relative_humidity_threshold_2(self):

        inputs = {
            "low": 55.0,
            "high": 105.0,
            "epsilon": 0.00001,
            "temperature": 85.1,
            "heat_threshold": 95.0,
        }
        expected = ["Relative humidity threshold: 75"]

        return self.attempt_cases(inputs, expected)

    @case_options(
        1,
        "Your code does not find the relative humidity threshold correctly",
        "Task find_relative_humidity_threshold error",
    )

    def test_find_relative_humidity_threshold_3(self):

        inputs = {
            "low": 26.3,
            "high": 85.0,
            "epsilon": 0.00001,
            "temperature": 98.5,
            "heat_threshold": 109.7,
        }
        expected = ["Relative humidity threshold: 45"]

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
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestProblemSetPartC))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestProblemSetPartD))

    runner = unittest.TextTestRunner(resultclass=Results_600, verbosity=2)
    result = runner.run(suite)

    output = result.getOutput()
    points_earned = round(result.getPoints(), 3)

    print(output)

    print(f"Total points: {points_earned} / {result.max_points}")
