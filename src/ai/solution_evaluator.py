from typing import Dict, List, Any, Callable
import time
import traceback


class SolutionEvaluator:
    """Evaluates user solutions against test cases and provides feedback."""
    
    def __init__(self):
        """Initialize the solution evaluator."""
        pass
    
    def evaluate(
        self,
        solution_func: Callable,
        test_cases: List[Dict[str, Any]],
        expected_time_complexity: str = "O(n)",
        expected_space_complexity: str = "O(n)"
    ) -> Dict[str, Any]:
        """
        Evaluate a solution against test cases.
        
        Args:
            solution_func: User's solution function
            test_cases: List of test cases with inputs and expected outputs
            expected_time_complexity: Expected time complexity (for reference)
            expected_space_complexity: Expected space complexity (for reference)
            
        Returns:
            Dict with evaluation results
        """
        results = {
            "success": True,
            "test_cases": [],
            "time_taken": 0,
            "feedback": [],
            "expected_time_complexity": expected_time_complexity,
            "expected_space_complexity": expected_space_complexity
        }
        
        start_time = time.time()
        
        # Run each test case
        for tc in test_cases:
            test_result = self._run_test_case(solution_func, tc)
            results["test_cases"].append(test_result)
            
            if not test_result["passed"]:
                results["success"] = False
        
        # Calculate total time
        results["time_taken"] = time.time() - start_time
        
        # Generate feedback
        results["feedback"] = self._generate_feedback(results)
        
        return results
    
    def _run_test_case(self, solution_func: Callable, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single test case.
        
        Args:
            solution_func: User's solution function
            test_case: Dict with inputs and expected output
            
        Returns:
            Dict with test case results
        """
        result = {
            "passed": False,
            "input": test_case["input"],
            "expected": test_case["expected"]
        }
        
        try:
            # Time the execution
            start_time = time.time()
            
            # Call the function with the input
            if isinstance(test_case["input"], dict):
                # If input is a dict, use it as keyword arguments
                actual_output = solution_func(**test_case["input"])
            elif isinstance(test_case["input"], list):
                # If input is a list, use it as positional arguments
                actual_output = solution_func(*test_case["input"])
            else:
                # Otherwise, use it as a single argument
                actual_output = solution_func(test_case["input"])
            
            execution_time = time.time() - start_time
            
            # Check if the output matches the expected output
            result["actual"] = actual_output
            result["execution_time"] = execution_time
            
            # Compare output with expected result
            result["passed"] = self._compare_outputs(actual_output, test_case["expected"])
            
            if not result["passed"]:
                result["error"] = f"Expected {test_case['expected']}, but got {actual_output}"
            
        except Exception as e:
            result["error"] = str(e)
            result["traceback"] = traceback.format_exc()
        
        return result
    
    def _compare_outputs(self, actual: Any, expected: Any) -> bool:
        """
        Compare actual output with expected output.
        
        Args:
            actual: Actual output from user's solution
            expected: Expected output
            
        Returns:
            True if outputs match, False otherwise
        """
        # Handle different types of outputs
        if isinstance(expected, list) and isinstance(actual, list):
            # For lists, check if they have the same elements
            if len(expected) != len(actual):
                return False
            
            # Sort both lists if they're lists of comparable elements
            try:
                return sorted(expected) == sorted(actual)
            except TypeError:
                # If not sortable, compare as is
                return expected == actual
            
        elif isinstance(expected, dict) and isinstance(actual, dict):
            # For dicts, check if they have the same key-value pairs
            return expected == actual
            
        else:
            # For other types, use equality
            return expected == actual
    
    def _generate_feedback(self, results: Dict[str, Any]) -> List[str]:
        """
        Generate feedback based on evaluation results.
        
        Args:
            results: Evaluation results
            
        Returns:
            List of feedback strings
        """
        feedback = []
        
        # Check overall success
        if results["success"]:
            feedback.append("Great job! Your solution passed all test cases.")
            
            # Add performance feedback
            feedback.append(f"Your solution ran in {results['time_taken']:.5f} seconds.")
            
        else:
            # Count failed test cases
            failed_count = sum(1 for tc in results["test_cases"] if not tc["passed"])
            total_count = len(results["test_cases"])
            
            feedback.append(f"Your solution passed {total_count - failed_count} out of {total_count} test cases.")
            
            # Add specific feedback for the first few failed test cases
            for i, tc in enumerate(results["test_cases"]):
                if not tc["passed"] and i < 3:  # Limit to first 3 failed cases
                    if "error" in tc:
                        feedback.append(f"Test case {i+1} failed: {tc['error']}")
                    else:
                        feedback.append(f"Test case {i+1} failed. Input: {tc['input']}, Expected: {tc['expected']}, Got: {tc['actual']}")
        
        return feedback


class AICodeReviewer:
    """
    AI-powered code reviewer that provides feedback on code quality.
    This is a placeholder for future implementation.
    """
    
    def __init__(self, api_key: str = None):
        """Initialize the AI code reviewer."""
        self.api_key = api_key
    
    def review_code(self, code: str, problem_description: str) -> List[str]:
        """
        Review code using AI and provide feedback.
        
        Args:
            code: User's code
            problem_description: Description of the problem
            
        Returns:
            List of feedback items
        """
        # This is a placeholder - in a real implementation, this would call an AI API
        return [
            "Your solution has good readability.",
            "Consider adding more comments to explain your approach.",
            "Check for edge cases like empty inputs or large values."
        ]