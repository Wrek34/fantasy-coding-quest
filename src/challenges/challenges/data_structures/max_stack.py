from typing import List, Dict, Any, Callable
from src.challenges.challenge_base import Challenge, DifficultyLevel, ChallengeType


class MaxStackChallenge(Challenge):
    """
    A challenge to implement a max stack data structure.
    """

    def __init__(self):
        description = """
        Deep in the Data Structure Mountains, you discover an ancient dwarven forge.
        
        The master blacksmith challenges you: "Build me a magical stack that can keep track of the largest value it contains at all times!"
        
        You must implement a class called 'MaxStack' with the following methods:
        
        - `__init__()`: Initialize your data structure
        - `push(x)`: Add element x to the top of the stack
        - `pop()`: Remove and return the element at the top of the stack
        - `top()`: Get the element at the top of the stack without removing it
        - `get_max()`: Get the maximum element in the stack
        
        Example:
        ```
        stack = MaxStack()
        stack.push(5)    # stack: [5]
        stack.push(1)    # stack: [5, 1]
        stack.push(7)    # stack: [5, 1, 7]
        stack.top()      # returns 7
        stack.get_max()  # returns 7
        stack.pop()      # returns 7, stack: [5, 1]
        stack.get_max()  # returns 5
        ```
        
        All operations should have O(1) time complexity.
        """

        hints = [
            "Consider how to efficiently track the maximum value as elements are pushed and popped.",
            "You could use an additional stack to keep track of the maximum values.",
            "When pushing a new element, you need to update the max if the new element is greater than or equal to the current max.",
            "When popping an element, you need to update the max if the popped element was the max."
        ]

        solution = """
class MaxStack:
    def __init__(self):
        self.stack = []        # Main stack to store elements
        self.max_stack = []    # Auxiliary stack to track maximum values
    
    def push(self, x):
        # Push element to main stack
        self.stack.append(x)
        
        # Update max_stack
        # If max_stack is empty or x is greater than or equal to current max,
        # push x to max_stack
        if not self.max_stack or x >= self.max_stack[-1]:
            self.max_stack.append(x)
    
    def pop(self):
        if not self.stack:
            return None
        
        # Pop from main stack
        val = self.stack.pop()
        
        # If popped value is the current max, pop from max_stack too
        if self.max_stack and val == self.max_stack[-1]:
            self.max_stack.pop()
        
        return val
    
    def top(self):
        if not self.stack:
            return None
        
        return self.stack[-1]
    
    def get_max(self):
        if not self.max_stack:
            return None
        
        return self.max_stack[-1]
        """

        test_cases = [
            {
                "input": [
                    {"method": "__init__", "args": []},
                    {"method": "push", "args": [5]},
                    {"method": "push", "args": [1]},
                    {"method": "push", "args": [7]},
                    {"method": "top", "args": []},
                    {"method": "get_max", "args": []},
                    {"method": "pop", "args": []},
                    {"method": "get_max", "args": []}
                ],
                "expected": [None, None, None, None, 7, 7, 7, 5]
            },
            {
                "input": [
                    {"method": "__init__", "args": []},
                    {"method": "push", "args": [2]},
                    {"method": "push", "args": [0]},
                    {"method": "push", "args": [3]},
                    {"method": "push", "args": [0]},
                    {"method": "get_max", "args": []},
                    {"method": "pop", "args": []},
                    {"method": "get_max", "args": []},
                    {"method": "pop", "args": []},
                    {"method": "get_max", "args": []}
                ],
                "expected": [None, None, None, None, None, 3, 0, 3, 3, 2]
            },
            {
                "input": [
                    {"method": "__init__", "args": []},
                    {"method": "push", "args": [3]},
                    {"method": "push", "args": [3]},
                    {"method": "get_max", "args": []},
                    {"method": "pop", "args": []},
                    {"method": "get_max", "args": []}
                ],
                "expected": [None, None, None, 3, 3, 3]
            }
        ]

        super().__init__(
            id="max-stack",
            name="The Dwarven Memory Forge",
            description=description,
            difficulty=DifficultyLevel.MEDIUM,
            challenge_type=ChallengeType.DATA_STRUCTURE,
            xp_reward=75,
            time_limit_seconds=45,
            test_cases=test_cases,
            hints=hints,
            solution=solution,
            area="Data Structure Mountains"
        )

    def verify_solution(self, user_solution: Callable) -> Dict[str, Any]:
        """
        Special verification for class implementations.
        """
        results = {
            "success": True,
            "test_cases": [],
            "time_taken": 0,
            "feedback": []
        }

        import time
        start_time = time.time()

        # Get the MaxStack class from the user's solution
        MaxStack = user_solution

        for i, tc in enumerate(self.test_cases):
            test_result = {
                "passed": True,
                "input": tc["input"],
                "expected": tc["expected"],
                "actual": []
            }

            try:
                obj = None

                for j, operation in enumerate(tc["input"]):
                    method_name = operation["method"]
                    args = operation["args"]

                    if method_name == "__init__":
                        obj = MaxStack()
                        test_result["actual"].append(None)
                    else:
                        if not obj:
                            raise ValueError("Object not initialized")

                        # Get the method from the object
                        method = getattr(obj, method_name)

                        # Call the method with the arguments
                        result = method(*args)
                        test_result["actual"].append(result)

                # Check if the actual results match the expected results
                if test_result["actual"] != tc["expected"]:
                    test_result["passed"] = False
                    test_result["error"] = f"Expected {tc['expected']}, but got {test_result['actual']}"
                    results["success"] = False

            except Exception as e:
                test_result["passed"] = False
                test_result["error"] = str(e)
                results["success"] = False

            results["test_cases"].append(test_result)

        results["time_taken"] = time.time() - start_time

        # Generate feedback
        if results["success"]:
            results["feedback"].append(
                "Great job! Your MaxStack implementation works correctly.")
            results["feedback"].append(
                f"Your solution ran in {results['time_taken']:.5f} seconds.")
        else:
            failed_count = sum(
                1 for tc in results["test_cases"] if not tc["passed"])
            results["feedback"].append(
                f"Your solution passed {len(self.test_cases) - failed_count} out of {len(self.test_cases)} test cases.")

            for i, tc in enumerate(results["test_cases"]):
                if not tc["passed"]:
                    results["feedback"].append(
                        f"Test case {i+1} failed: {tc.get('error', 'Unknown error')}")

        return results
