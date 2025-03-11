from typing import List, Dict, Any, Callable
from src.challenges.challenge_base import Challenge, DifficultyLevel, ChallengeType


class HelloWorldChallenge(Challenge):
    """
    A super simple challenge for absolute beginners to get familiar with the game interface.
    """

    def __init__(self):
        description = """
        Welcome to the Algorithm Forest, brave adventurer!
        
        Before you embark on your journey, let's make sure you can communicate with the magical beings of this realm.
        
        Create a function called 'hello_world' that:
        - Takes no parameters
        - Returns the string: "Hello, magical world!"
        
        This is the simplest of spells, but every great algorithm wizard starts somewhere!
        
        Example:
        - Input: No input
        - Output: "Hello, magical world!"
        
        Hint: In Python, you can create a function like this:
        
        ```python
        def function_name():
            # Your code here
            return something
        ```
        """

        hints = [
            "Your function should be named 'hello_world' with no parameters.",
            "To return a string, use the return keyword followed by the string in quotes.",
            "The exact string to return is: \"Hello, magical world!\"",
            "Make sure to include the exclamation mark!"
        ]

        solution = """
        def hello_world():
            return "Hello, magical world!"
        """

        test_cases = [
            {
                "input": {},
                "expected": "Hello, magical world!"
            }
        ]

        super().__init__(
            id="hello-world",
            name="The Greeting Spell",
            description=description,
            difficulty=DifficultyLevel.EASY,
            challenge_type=ChallengeType.ALGORITHM,
            xp_reward=10,
            time_limit_seconds=60,  # Very generous time limit for beginners
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
        results = evaluator.evaluate(
            solution_func=user_solution,
            test_cases=self.test_cases
        )

        # Add extra beginner-friendly feedback
        if results["success"]:
            results["feedback"].append(
                "Congratulations on completing your first challenge!")
            results["feedback"].append(
                "This is the beginning of your journey. You'll tackle more complex challenges as you progress.")
        else:
            results["feedback"].append(
                "Don't worry if you didn't get it right the first time. Coding is all about learning from mistakes.")
            results["feedback"].append(
                "Check if your function name is exactly 'hello_world' and that you're returning the exact string \"Hello, magical world!\"")

        return results
