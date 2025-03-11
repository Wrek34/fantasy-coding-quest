from typing import List, Dict, Any, Callable
from src.challenges.challenge_base import Challenge, DifficultyLevel, ChallengeType


class BinarySearchChallenge(Challenge):
    """
    A challenge to implement the binary search algorithm.
    """

    def __init__(self):
        description = """
        In the Algorithm Forest, you come across an ancient library guarded by a sphinx.
        
        "To pass, you must find a specific tome in this vast collection," says the sphinx.
        "But you must use the ancient technique of binary search to find it quickly."
        
        You must write a function called 'binary_search' that accepts:
        - arr (List[int]): A sorted array of integers
        - target (int): The value to search for
        
        Your function should return:
        - result (int): The index of the target if found, or -1 if not found
        
        Example:
        - Input: arr = [1, 3, 5, 7, 9], target = 5
        - Output: 2 (because arr[2] = 5)
        """

        hints = [
            "Remember that binary search only works on sorted arrays.",
            "Start by defining the search space with left and right pointers.",
            "Calculate the middle index and compare the middle element with the target.",
            "If the middle element is the target, return its index.",
            "If the target is less than the middle element, search the left half.",
            "If the target is greater than the middle element, search the right half."
        ]

        solution = """
        def binary_search(arr, target):
            left, right = 0, len(arr) - 1
            
            while left <= right:
                mid = (left + right) // 2
                
                # Check if target is present at mid
                if arr[mid] == target:
                    return mid
                
                # If target is greater, ignore left half
                elif arr[mid] < target:
                    left = mid + 1
                
                # If target is smaller, ignore right half
                else:
                    right = mid - 1
            
            # Element is not present in the array
            return -1
        """

        test_cases = [
            {
                "input": {"arr": [1, 3, 5, 7, 9], "target": 5},
                "expected": 2
            },
            {
                "input": {"arr": [1, 3, 5, 7, 9], "target": 9},
                "expected": 4
            },
            {
                "input": {"arr": [1, 3, 5, 7, 9], "target": 1},
                "expected": 0
            },
            {
                "input": {"arr": [1, 3, 5, 7, 9], "target": 4},
                "expected": -1
            },
            {
                "input": {"arr": [1, 3, 5, 7, 9], "target": 10},
                "expected": -1
            }
        ]

        super().__init__(
            id="binary-search",
            name="The Ancient Tome Search",
            description=description,
            difficulty=DifficultyLevel.EASY,
            challenge_type=ChallengeType.ALGORITHM,
            xp_reward=50,
            time_limit_seconds=30,
            test_cases=test_cases,
            hints=hints,
            solution=solution,
            area="Algorithm Forest"
        )

    def verify_solution(self, user_solution: Callable) -> Dict[str, Any]:
        """
        Run test cases against the user's solution.

        Args:
            user_solution: User's solution function

        Returns:
            Dict with verification results
        """
        from src.ai.solution_evaluator import SolutionEvaluator

        evaluator = SolutionEvaluator()
        return evaluator.evaluate(
            solution_func=user_solution,
            test_cases=self.test_cases,
            expected_time_complexity="O(log n)",
            expected_space_complexity="O(1)"
        )
