from typing import List, Dict, Any, Callable
from src.challenges.challenge_base import Challenge, DifficultyLevel, ChallengeType


class LinkedListCycleChallenge(Challenge):
    """
    A challenge to detect a cycle in a linked list.
    """

    def __init__(self):
        description = """
        In the Data Structure Mountains, you encounter a peculiar puzzle at a crossroads.
        
        A wise old mountain sage presents you with a magical chain of interconnected links.
        "This chain may loop back on itself," the sage explains. "You must determine if it does."
        
        You must write a function called 'has_cycle' that accepts:
        - head: The head of a linked list
        
        Your function should return:
        - result (bool): True if the linked list has a cycle, False otherwise
        
        The linked list is represented with the following class:
        
        ```python
        class ListNode:
            def __init__(self, val=0, next=None):
                self.val = val
                self.next = next
        ```
        
        Note: You cannot modify the linked list.
        
        Example:
        - Input: head = [3,2,0,-4] with a cycle where the tail connects to node at index 1
        - Output: True (because there is a cycle in the linked list)
        """

        hints = [
            "Consider using two pointers that move at different speeds.",
            "What happens if one pointer moves twice as fast as the other?",
            "If there's a cycle, the fast pointer will eventually catch up to the slow pointer.",
            "This is the classic 'tortoise and hare' algorithm for cycle detection."
        ]

        solution = """
        def has_cycle(head):
            if not head or not head.next:
                return False
            
            # Initialize two pointers, slow and fast
            slow = head
            fast = head.next
            
            # Move slow one step and fast two steps at a time
            while slow != fast:
                # If fast reaches the end, there's no cycle
                if not fast or not fast.next:
                    return False
                
                slow = slow.next
                fast = fast.next.next
            
            # If we exit the while loop, slow and fast have met, indicating a cycle
            return True
        """

        # Special test case setup for linked lists
        test_code = """
# ListNode definition for testing
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def create_linked_list(values, pos):
    if not values:
        return None
    
    # Create nodes
    nodes = [ListNode(val) for val in values]
    
    # Link nodes
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    
    # Create cycle if pos is valid
    if pos >= 0 and pos < len(nodes):
        nodes[-1].next = nodes[pos]
    
    return nodes[0]

# Test case 1: List with cycle
head1 = create_linked_list([3, 2, 0, -4], 1)
result1 = has_cycle(head1)
assert result1 == True, f"Expected True, got {result1}"

# Test case 2: List with no cycle
head2 = create_linked_list([1, 2, 3, 4], -1)
result2 = has_cycle(head2)
assert result2 == False, f"Expected False, got {result2}"

# Test case 3: Single node with cycle to itself
head3 = create_linked_list([1], 0)
result3 = has_cycle(head3)
assert result3 == True, f"Expected True, got {result3}"

# Test case 4: Single node with no cycle
head4 = create_linked_list([1], -1)
result4 = has_cycle(head4)
assert result4 == False, f"Expected False, got {result4}"

# Test case 5: Empty list
head5 = None
result5 = has_cycle(head5)
assert result5 == False, f"Expected False, got {result5}"

print("All test cases passed!")
"""

        # Since linked list challenges can't easily use the standard test case format,
        # we'll use a special format that includes test code that will be executed directly
        test_cases = [
            {
                "special_test_code": test_code
            }
        ]

        super().__init__(
            id="linked-list-cycle",
            name="The Endless Chain",
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
        Run test cases against the user's solution.

        For linked list problems, we need a special verification method
        that executes the test code directly.
        """
        results = {
            "success": True,
            "test_cases": [],
            "time_taken": 0,
            "feedback": []
        }

        import time
        start_time = time.time()

        for tc in self.test_cases:
            if "special_test_code" in tc:
                # Create a namespace with the user's solution
                test_namespace = {"has_cycle": user_solution}

                try:
                    # Execute the test code
                    exec(tc["special_test_code"], test_namespace)

                    # If we get here, all assertions passed
                    results["test_cases"].append({
                        "passed": True,
                        "execution_time": time.time() - start_time
                    })

                except AssertionError as e:
                    results["success"] = False
                    results["test_cases"].append({
                        "passed": False,
                        "error": str(e)
                    })

                except Exception as e:
                    results["success"] = False
                    results["test_cases"].append({
                        "passed": False,
                        "error": f"Error: {str(e)}"
                    })

        results["time_taken"] = time.time() - start_time

        # Generate feedback
        if results["success"]:
            results["feedback"].append(
                "Great job! Your solution correctly detects cycles in linked lists.")
            results["feedback"].append(
                f"Your solution ran in {results['time_taken']:.5f} seconds.")
        else:
            failed_count = sum(
                1 for tc in results["test_cases"] if not tc.get("passed", False))
            total_count = len(results["test_cases"])
            results["feedback"].append(
                f"Your solution passed {total_count - failed_count} out of {total_count} test cases.")

            for i, tc in enumerate(results["test_cases"]):
                if not tc.get("passed", False) and i < 3:  # Limit to first 3 failed cases
                    results["feedback"].append(
                        f"Test case {i+1} failed: {tc.get('error', 'Unknown error')}")

        return results
