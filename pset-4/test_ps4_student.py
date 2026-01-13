import unittest
from unittest.mock import patch, MagicMock
import sys
import io
import re
from ps4 import *

class TestCreatePrizeDict(unittest.TestCase):
    def setUp(self):
        self.cases = list(range(1, 27))
        self.amounts = [
            0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 750, 1000, 
            5000, 10000, 25000, 50000, 75000, 100000, 200000, 300000, 400000, 
            500000, 750000, 1000000
        ]
        self.points = 1
    
    def test_create_prize_dict_1(self):
        """
        Test create_prize_dict function to ensure it creates a dictionary with unique values.
        """
        self.failure_message = "create_prize_dict() does not return a dictionary with unique values"
        self.error_message = "create_prize_dict() raised an unexpected error"
        prizes = create_prize_dict()
        self.assertEqual(len(prizes), 26)
        # All values should be unique
        self.assertEqual(len(set(prizes.values())), 26)
        # Set of values in the returned dict should match the set of amounts
        self.assertEqual(set(prizes.values()), set(self.amounts))

class TestValidateUserBriefcaseChoice(unittest.TestCase):
    def setUp(self):
        # Mock prize data
        self.prizes = {i: i * 1000 for i in range(1, 27)}
        # Initial case status
        self.case_status = {i: 'closed' for i in range(1, 27)}
        # Player case
        self.case_status[1] = 'player_case'
        self.points = 1

    def test_validate_users_briefcase_choice_1_valid_select(self):
        """
        Test validate_users_briefcase_choice function with valid input.
        """
        self.failure_message = "validate_users_briefcase_choice() raised a ValueError unexpectedly for valid input"
        self.error_message = "validate_users_briefcase_choice() raised an unexpected error for valid input"
        try:
            validate_users_briefcase_choice('5', self.case_status, 'select')
        except ValueError:
            self.fail("validate_users_briefcase_choice() raised ValueError unexpectedly")

    def test_validate_users_briefcase_choice_2_invalid_select(self):
        """
        Test validate_users_briefcase_choice function with invalid input.
        """
        self.failure_message = "validate_users_briefcase_choice() did not raise a ValueError for invalid input"
        self.error_message = "validate_users_briefcase_choice() raised an error that is not a ValueError for invalid input"
        with self.assertRaises(ValueError):
            validate_users_briefcase_choice('27', self.case_status, 'select')
        
    def test_validate_users_briefcase_choice_3_non_integer_select(self):
        """
        Test validate_users_briefcase_choice function with non-integer input.
        """
        self.failure_message = "validate_users_briefcase_choice() did not raise a ValueError for non-integer input"
        self.error_message = "validate_users_briefcase_choice() raised an error that is not a ValueError for non-integer input"
        with self.assertRaises(ValueError):
            validate_users_briefcase_choice('a', self.case_status, 'select')

    def test_validate_users_briefcase_choice_4_valid_whitespace_select(self):
        """
        Test validate_users_briefcase_choice function with valid input containing whitespace.
        """
        self.failure_message = "validate_users_briefcase_choice() did not strip whitespace from input"
        self.error_message = "validate_users_briefcase_choice() raised an unexpected error for input with whitespace"
        try:
            validate_users_briefcase_choice('  5  ', self.case_status, 'select')
        except ValueError:
            self.fail("validate_users_briefcase_choice() raised ValueError unexpectedly")
        
    def test_validate_users_briefcase_choice_5_player_case_open(self):
        """
        Test validate_users_briefcase_choice function with player case and open case action.
        """
        self.failure_message = "validate_users_briefcase_choice() did not raise a ValueError for player case and open action"
        self.error_message = "validate_users_briefcase_choice() raised an error that is not a ValueError for player case and open action"
        with self.assertRaises(ValueError):
            validate_users_briefcase_choice('1', self.case_status, 'open')
        
    

class TestSelectBriefcase(unittest.TestCase):
    def setUp(self):
        # Mock prize data
        self.prizes = {i: i * 1000 for i in range(1, 27)}
        # Initial case status
        self.case_status = {i: 'closed' for i in range(1, 27)}
        self.points = 1

    @patch('builtins.input', side_effect=['5'])
    def test_select_briefcase_1_valid(self, mock_input):
        """
        Test select_briefcase function with valid input.
        """
        self.failure_message = "select_briefcase() raised a ValueError unexpectedly for valid input"
        self.error_message = "select_briefcase() raised an unexpected error for valid input"
        player_case = select_briefcase(self.case_status)
        self.assertEqual(player_case, 5)
        self.assertEqual(self.case_status[5], 'player_case')

    @patch('builtins.input', side_effect=['27', '5'])
    @patch('builtins.print')
    def test_select_briefcase_2_invalid_then_valid(self, mock_print, mock_input):
        """
        Test select_briefcase with invalid and then valid input.
        """
        # Test continues with valid input '5' despite the invalid input of '27'
        self.failure_message = "select_briefcase() raised a ValueError unexpectedly for invalid input followed by valid input"
        self.error_message = "select_briefcase() raised an unexpected error for invalid input followed by valid input"
        player_case = select_briefcase(self.case_status)
        self.assertEqual(player_case, 5)
        self.assertEqual(self.case_status[5], 'player_case')

    @patch('builtins.input', side_effect=['a', '5'])
    @patch('builtins.print')
    def test_select_briefcase_3_non_integer_input(self, mock_print, mock_input):
        """
        Test select_briefcase function with non-integer input followed by valid input.
        """
        self.failure_message = "select_briefcase() raised a ValueError unexpectedly for non-integer input followed by valid input"
        self.error_message = "select_briefcase() raised an unexpected error for non-integer input followed by valid input"
        # Test continues with valid input '5' despite the non-integer input 'a'
        player_case = select_briefcase(self.case_status)
        self.assertEqual(player_case, 5)
        self.assertEqual(self.case_status[5], 'player_case')

    @patch('builtins.input', side_effect=['  5  '])
    def test_select_briefcase_4_with_whitespace(self, mock_input):
        """
        Test select_briefcase function with input containing extra whitespace.
        """
        self.failure_message = "select_briefcase() did not strip whitespace from input"
        self.error_message = "select_briefcase() raised an unexpected error for input with whitespace"
        player_case = select_briefcase(self.case_status)
        self.assertEqual(player_case, 5)  # The function should strip the whitespace and correctly select case 5
        self.assertEqual(self.case_status[5], 'player_case')
        

# Class for testing open_briefcases function
class TestOpenBriefcases(unittest.TestCase):
    def setUp(self):
        self.cases = list(range(1, 27))
        self.amounts = [
            0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 750, 1000, 
            5000, 10000, 25000, 50000, 75000, 100000, 200000, 300000, 400000, 
            500000, 750000, 1000000
        ]
        self.prizes = create_prize_dict()
        self.case_status = {case: 'closed' for case in self.cases}
        # Example: Case 1 is the player's case
        self.case_status[1] = 'player_case'
        self.points = 1
    
    @patch('builtins.input', side_effect=['2', '3'])
    # Mock stdout to suppress output
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_open_briefcases_1_valid(self, mock_stdout, mock_input):
        """
        Test open_briefcases with valid input cases.
        """
        self.failure_message = "open_briefcases() raised a ValueError unexpectedly for valid input"
        self.error_message = "open_briefcases() raised an unexpected error for valid input"
        open_briefcases(self.prizes, self.case_status, 2, 1)
        self.assertEqual(self.case_status[2], 'opened')
        self.assertEqual(self.case_status[3], 'opened')

    @patch('builtins.input', side_effect=['abc', '2'])
    # Mock stdout to suppress output
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_open_briefcases_2_non_integer_input(self, mock_stdout, mock_input):
        """
        Test open_briefcases with non-integer input followed by valid input.
        """
        self.failure_message = "open_briefcases() raised a ValueError unexpectedly for non-integer input followed by valid input"
        self.error_message = "open_briefcases() raised an unexpected error for non-integer input followed by valid input"
        open_briefcases(self.prizes, self.case_status, 1, 1)
        self.assertEqual(self.case_status[2], 'opened')
        

    @patch('builtins.input', side_effect=['30', '2'])
    # Mock stdout to suppress output
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_open_briefcases_3_out_of_range(self, mock_stdout, mock_input):
        """
        Test open_briefcases with out-of-range input followed by valid input.
        """
        self.failure_message = "open_briefcases() raised a ValueError unexpectedly for out-of-range input followed by valid input"
        self.error_message = "open_briefcases() raised an unexpected error for out-of-range input followed by valid input"
        open_briefcases(self.prizes, self.case_status, 1, 1)
        self.assertEqual(self.case_status[2], 'opened')

    @patch('builtins.input', side_effect=['1', '2'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_open_briefcases_4_player_case(self, mock_stdout, mock_input):
        """
        Test that open_briefcases does not immediately open the player's case.
        """
        self.failure_message = "open_briefcases() opened the player's case immediately"
        self.error_message = "open_briefcases() raised an unexpected error when opening the player's case"
        # Player's case is case 1
        self.case_status[1] = 'player_case'
        open_briefcases(self.prizes, self.case_status, 1, 1)
        self.assertEqual(self.case_status[1], 'player_case')

class TestAutoDecisionHelper(unittest.TestCase):
    def setUp(self):
        self.cases = list(range(1, 27))
        self.points = 1
        self.prizes = create_prize_dict()
        self.case_status = {case: 'closed' for case in self.cases}
        self.case_status[1] = 'player_case'
        # Open some cases
        self.case_status[2] = 'opened'
        self.case_status[3] = 'opened'
        self.case_status[4] = 'opened'
        self.case_status[5] = 'opened'
        self.case_status[6] = 'opened'
        self.case_status[7] = 'opened'
        self.round_num = 1
    
    def test_auto_decision_helper_1(self):
        """
        Test auto_decision_helper returns 'yes' or 'no'
        """
        self.failure_message = "auto_decision_helper() is not returning 'yes' or 'no'"
        self.error_message = "auto_decision_helper() raised an unexpected error"
        # if the error is NotImplementedError, update failure message
        try:
            decision = auto_decision_helper(self.prizes, self.case_status, 99184, self.round_num)
            self.assertIn(decision, ['yes', 'no'])
        except NotImplementedError:
            self.fail("auto_decision_helper() is not implemented")
        except Exception as e:
            self.fail(f"Unexpected error: {e}")


class Results_600(unittest.TextTestResult):
    """
    Custom test result class to capture output and points.
    """

    def __init__(self, *args, **kwargs):
        super(Results_600, self).__init__(*args, **kwargs)
        self.output = []
        self.points = 0
        self.max_points = 0

    def addSuccess(self, test):
        method = getattr(test, getattr(test, "_testMethodName"))
        # Fetch points from the test class
        pts = getattr(test, "points", 0)
        self.points += pts
        self.max_points += pts
        self.output.append(f"✅ [+{pts}] {test} passed!\n")
        super().addSuccess(test)

    def addFailure(self, test, err):
        # Fetch points from the test class
        pts = getattr(test, "points", 0)
        failure_message = getattr(test, "failure_message", f"{test} failed")
        self.output.append(f"❌ {failure_message}: {err[1]}\n")
        self.max_points += pts
        super().addFailure(test, err)

    def addError(self, test, err):
        # Fetch points from the test class
        pts = getattr(test, "points", 0)
        error_message = getattr(test, "error_message", f"{test} failed")
        self.output.append(f"❌ {error_message}: {err[0]}\n")
        self.max_points += pts
        super().addError(test, err)

    def getOutput(self):
        if self.points > 0:
            if self.points == self.max_points:
                self.output.append(f"\n✅ [{self.points}/{self.max_points}] All tests passed!\n")
            else:
                self.output.append(f"\n❌ [{self.points}/{self.max_points}] Some tests failed!\n")
        else:
            self.output.append("\n❌ No tests passed!\n")
        return "\n".join(self.output)

    def getPoints(self):
        return self.points


# Main test suite runner
if __name__ == '__main__':
    print("Running Unit Tests!")
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCreatePrizeDict))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestValidateUserBriefcaseChoice))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSelectBriefcase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOpenBriefcases))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAutoDecisionHelper))

    runner = unittest.TextTestRunner(resultclass=Results_600, verbosity=2)
    result = runner.run(suite)

    output = result.getOutput()
    points_earned = round(result.getPoints(), 3)
    print("=====================================================")
    print("Scroll up to see more details on any failures/errors.")
    print("=====================================================")
    print(output)
    print(f"Total points earned: {points_earned}")
