from typing import List, Optional
import random


class SimpleHintGenerator:
    """
    A simple hint generator that provides predefined hints.
    This will be replaced with an AI-powered version later.
    """
    
    def __init__(self):
        """Initialize the hint generator with generic hints."""
        self.generic_hints = {
            "arrays": [
                "Consider using a two-pointer approach.",
                "Can you solve this in-place to optimize space complexity?",
                "Think about edge cases like empty arrays or arrays with a single element.",
                "Have you considered using a hash map to reduce time complexity?"
            ],
            "linked_lists": [
                "Consider using a fast and slow pointer technique.",
                "Would a dummy head node simplify your code?",
                "Be careful with null pointers when manipulating links.",
                "Think about whether a recursive solution might be cleaner."
            ],
            "trees": [
                "Consider if a depth-first or breadth-first approach is more appropriate.",
                "Recursive solutions often work well with tree problems.",
                "Check if you need to handle unbalanced or degenerate trees.",
                "Is there a way to avoid using extra space?"
            ],
            "dynamic_programming": [
                "Try identifying the overlapping subproblems.",
                "Can you define a recurrence relation?",
                "Consider using memoization to avoid redundant calculations.",
                "Think about the base cases of your recursion."
            ],
            "sorting": [
                "Consider the trade-offs between different sorting algorithms.",
                "Can you sort in-place to save memory?",
                "Is stability important for this sorting problem?",
                "Could you use a non-comparison-based sort?"
            ],
            "searching": [
                "Consider if the input has any special properties you can exploit.",
                "Is the data sorted? If so, binary search might be useful.",
                "Think about space complexity - can you search in-place?",
                "Consider using two pointers or a sliding window approach."
            ]
        }
    
    def generate_hints(
        self, 
        problem_type: str, 
        specific_hints: List[str] = None, 
        difficulty: int = 1,
        num_hints: int = 3
    ) -> List[str]:
        """
        Generate a list of hints for a given problem.
        
        Args:
            problem_type: Type of problem (arrays, linked_lists, etc.)
            specific_hints: Optional list of problem-specific hints
            difficulty: Difficulty level (1-5)
            num_hints: Number of hints to generate
            
        Returns:
            List of hints, starting with more general hints and getting more specific
        """
        hints = []
        
        # If specific hints are provided, use those
        if specific_hints:
            hints.extend(specific_hints)
            
            # If not enough specific hints, add generic ones
            if len(hints) < num_hints:
                generic_type = problem_type.lower()
                if generic_type in self.generic_hints:
                    # Add relevant generic hints that aren't too similar to specific ones
                    for hint in self.generic_hints[generic_type]:
                        if len(hints) >= num_hints:
                            break
                        # Simple check to avoid duplicates
                        if not any(self._is_similar(hint, existing) for existing in hints):
                            hints.append(hint)
        
        # If no specific hints or not enough hints, add generic ones
        while len(hints) < num_hints:
            generic_type = problem_type.lower()
            if generic_type in self.generic_hints and self.generic_hints[generic_type]:
                hint = random.choice(self.generic_hints[generic_type])
                if hint not in hints:
                    hints.append(hint)
            else:
                # If we don't have enough hints of the right type, add a general coding hint
                general_hints = [
                    "Break down the problem into smaller steps.",
                    "Consider edge cases in your solution.",
                    "Think about the time and space complexity of your approach.",
                    "Try working through a simple example by hand first.",
                    "Can you simplify the problem to solve a smaller version first?"
                ]
                hint = random.choice(general_hints)
                if hint not in hints:
                    hints.append(hint)
        
        return hints[:num_hints]
    
    def _is_similar(self, hint1: str, hint2: str, threshold: float = 0.7) -> bool:
        """
        Simple function to check if two hints are similar.
        In a real implementation, this could use more sophisticated NLP techniques.
        
        Args:
            hint1: First hint
            hint2: Second hint
            threshold: Similarity threshold (0-1)
            
        Returns:
            True if hints are similar, False otherwise
        """
        # Very basic similarity check
        words1 = set(hint1.lower().split())
        words2 = set(hint2.lower().split())
        
        if not words1 or not words2:
            return False
            
        intersection = words1.intersection(words2)
        similarity = len(intersection) / max(len(words1), len(words2))
        
        return similarity > threshold


class AIHintGenerator:
    """
    AI-powered hint generator using a language model.
    This is a placeholder for future implementation.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI hint generator.
        
        Args:
            api_key: Optional API key for the language model service
        """
        self.api_key = api_key
        self.fallback_generator = SimpleHintGenerator()
    
    def generate_hints(
        self,
        problem_description: str,
        problem_type: str,
        code_so_far: Optional[str] = None,
        difficulty: int = 1,
        num_hints: int = 3
    ) -> List[str]:
        """
        Generate hints using AI based on the problem and user's code.
        
        Args:
            problem_description: Description of the problem
            problem_type: Type of problem (arrays, linked_lists, etc.)
            code_so_far: User's code so far, if any
            difficulty: Difficulty level (1-5)
            num_hints: Number of hints to generate
            
        Returns:
            List of hints, from general to specific
        """
        # This is a placeholder - in a real implementation, this would call an AI API
        # For now, fall back to the simple hint generator
        return self.fallback_generator.generate_hints(
            problem_type=problem_type,
            difficulty=difficulty,
            num_hints=num_hints
        )