import time
from typing import List, Dict, Any, Callable
from src.challenges.challenge_base import Challenge, DifficultyLevel, ChallengeType


class SumOfTwoChallenge(Challenge):
    """
    A very simple challenge for beginners that includes a step-by-step explanation.
    """

    def __init__(self):
        description = """
        At the entrance to the Algorithm Forest, a friendly sprite challenges you with a simple task.
        
        "Create a function called 'sum_of_two' that takes two numbers and returns their sum," the sprite explains.
        
        Step-by-step guide:
        
        1. Create a function named 'sum_of_two' that takes two parameters: a and b
        2. Inside the function, add the two numbers together
        3. Return the result
        
        Example:
        - Input: a = 5, b = 3
        - Output: 8 (because 5 + 3 = 8)
        
        Here's a template to get you started:
        
        ```python
        def sum_of_two(a, b):
            # Your code here
            pass
        ```
        
        Simply replace the "pass" with your code to add a and b, then return the result.
        """

        hints = [
            "To add two numbers in Python, use the + operator: a + b",
            "The return statement sends a value back from your function: return result",
            "Your entire solution could be just one line!",
            "The solution is: return a + b"
        ]

        solution = """
        def sum_of_two(a, b):
            return a + b
        """

        test_cases = [
            {
                "input": {"a": 5, "b": 3},
                "expected": 8
            },
            {
                "input": {"a": 10, "b": -5},
                "expected": 5
            },
            {
                "input": {"a": 0, "b": 0},
                "expected": 0
            }
        ]

        super().__init__(
            id="sum-of-two",
            name="The Addition Spell",
            description=description,
            difficulty=DifficultyLevel.EASY,
            challenge_type=ChallengeType.ALGORITHM,
            xp_reward=20,
            time_limit_seconds=60,  # Very generous time limit for beginners
            test_cases=test_cases,
            hints=hints,
            solution=solution,
            area="Algorithm Forest"
        )

    def verify_solution(self, user_solution: Callable) -> Dict[str, Any]:
        """Run test cases against the user's solution."""
        from src.ai.solution_evaluator import SolutionEvaluator

        evaluator = SolutionEvaluator()
        results = evaluator.evaluate(
            solution_func=user_solution,
            test_cases=self.test_cases
        )

        # Add beginner-friendly explanation of the solution
        if results["success"]:
            results["feedback"].append(
                "Great job! You've mastered the addition spell.")
            results["feedback"].append("Let's understand what your code did:")
            results["feedback"].append(
                "1. You created a function that takes two parameters (a and b)")
            results["feedback"].append(
                "2. You added them together with the + operator")
            results["feedback"].append(
                "3. You returned the result to the caller")
            results["feedback"].append(
                "This pattern of taking inputs, processing them, and returning a result is the foundation of most functions you'll write!")

        return results
