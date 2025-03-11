from typing import List, Dict, Any, Callable
from src.challenges.challenge_base import Challenge, DifficultyLevel, ChallengeType


class TwoSumChallenge(Challenge):
    """
    A challenge to implement the two sum algorithm.
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
    """
    
    def __init__(self):
        description = """
        In the mystical Algorithm Forest, you encounter a peculiar puzzle guarded by a wise old owl.
        
        "Find the two numbers in this array that sum to the target value," hoots the owl.
        "Return their indices, and you may pass through to your next challenge."
        
        You must write a function called 'two_sum' that accepts:
        - nums (List[int]): A list of integers
        - target (int): The target sum
        
        Your function should return:
        - result (List[int]): A list containing the indices of the two numbers that add up to the target
        
        You may assume:
        - Each input has exactly one solution
        - You may not use the same element twice
        - The answer can be returned in any order
        
        Example:
        - Input: nums = [2, 7, 11, 15], target = 9
        - Output: [0, 1] (because nums[0] + nums[1] = 2 + 7 = 9)
        """
        
        hints = [
            "Try the simplest approach first: check every pair of numbers in the array.",
            "Can you use a data structure to reduce the number of comparisons needed?",
            "Consider using a dictionary (hash map) to store numbers you've seen before."
        ]
        
        solution = """
        def two_sum(nums, target):
            # Create a dictionary to store numbers and their indices
            num_dict = {}
            
            # Iterate through the array
            for i, num in enumerate(nums):
                # Calculate the complement (the number we need to find)
                complement = target - num
                
                # Check if the complement is in the dictionary
                if complement in num_dict:
                    # Return the indices of the two numbers
                    return [num_dict[complement], i]
                
                # Add the current number and its index to the dictionary
                num_dict[num] = i
            
            # No solution found (per the problem, this should not happen)
            return []
        """
        
        test_cases = [
            {
                "input": {"nums": [2, 7, 11, 15], "target": 9},
                "expected": [0, 1]
            },
            {
                "input": {"nums": [3, 2, 4], "target": 6},
                "expected": [1, 2]
            },
            {
                "input": {"nums": [3, 3], "target": 6},
                "expected": [0, 1]
            },
            {
                "input": {"nums": [1, 2, 3, 4, 5], "target": 9},
                "expected": [3, 4]
            },
            {
                "input": {"nums": [-1, -2, -3, -4, -5], "target": -8},
                "expected": [2, 4]
            }
        ]
        
        super().__init__(
            id="two-sum",
            name="The Twin Sum Riddle",
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
            expected_time_complexity="O(n)",
            expected_space_complexity="O(n)"
        )