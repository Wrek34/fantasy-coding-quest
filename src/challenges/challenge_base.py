from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Any, Callable, Optional
import time
import inspect


class DifficultyLevel(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    EPIC = "Epic"


class ChallengeType(Enum):
    ALGORITHM = "Algorithm"
    DATA_STRUCTURE = "Data Structure"
    SYSTEM_DESIGN = "System Design"
    DATABASE = "Database"
    DEBUGGING = "Debugging"


class Challenge(ABC):
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        difficulty: DifficultyLevel,
        challenge_type: ChallengeType,
        xp_reward: int,
        time_limit_seconds: int = 0,  # 0 means no time limit
        test_cases: List[Dict[str, Any]] = None,
        hints: List[str] = None,
        solution: str = None,
        area: str = "Algorithm Forest",
        primary_skill: str = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.challenge_type = challenge_type
        self.xp_reward = xp_reward
        self.time_limit_seconds = time_limit_seconds
        self.test_cases = test_cases or []
        self.hints = hints or []
        self.solution = solution
        self.area = area
        self.primary_skill = primary_skill
        
        # Metadata for tracking
        self.times_attempted = 0
        self.times_completed = 0
        self.best_time = float('inf')
    
    def get_fantasy_description(self) -> str:
        """Return a fantasy-themed description of the challenge."""
        difficulty_prefix = {
            DifficultyLevel.EASY: "A novice's task",
            DifficultyLevel.MEDIUM: "A skilled adventurer's challenge",
            DifficultyLevel.HARD: "A hero's trial",
            DifficultyLevel.EPIC: "A legendary quest"
        }
        
        return f"""{difficulty_prefix[self.difficulty]} in the {self.area}:
        
{self.name}

{self.description}

Reward: {self.xp_reward} XP
Time Limit: {"None" if self.time_limit_seconds == 0 else f"{self.time_limit_seconds} seconds"}
"""
    
    def get_hint(self, hint_level: int = 0) -> str:
        """Get a hint for the challenge based on the hint level."""
        if not self.hints or hint_level >= len(self.hints):
            return "No more hints available for this challenge."
        return self.hints[hint_level]
    
    def attempt_solution(self, user_solution: Callable) -> Dict[str, Any]:
        """
        Attempt a solution for this challenge. This method calls verify_solution
        which should be implemented by subclasses.
        
        Args:
            user_solution: User's solution function
            
        Returns:
            Dict with verification results
        """
        try:
            # Measure the time taken
            start_time = time.time()
            
            # Verify the solution
            results = self.verify_solution(user_solution)
            
            # Add the time taken
            results["time_taken"] = time.time() - start_time
            
            return results
        except Exception as e:
            # Return error if something went wrong
            return {
                "success": False,
                "feedback": [f"Error evaluating solution: {str(e)}"],
                "time_taken": 0
            }
    
    @abstractmethod
    def verify_solution(self, user_solution: Callable) -> Dict[str, Any]:
        """
        Run test cases against the user's solution.
        This method should be overridden by subclasses.
        
        Args:
            user_solution: User's solution function
            
        Returns:
            Dict with verification results
        """
        raise NotImplementedError("Challenge subclasses must implement verify_solution method")
    
    def attempt(self, user_solution_code: str) -> Dict[str, Any]:
        """
        Process a user's attempt at solving the challenge.
        
        Args:
            user_solution_code: String containing the user's Python code
            
        Returns:
            Dict containing results, success/failure, time taken, etc.
        """
        self.times_attempted += 1
        start_time = time.time()
        
        # Compile the user's code
        try:
            user_solution_namespace = {}
            exec(user_solution_code, user_solution_namespace)
            
            # Find the main function in the user's code
            user_solution = None
            for name, obj in user_solution_namespace.items():
                if callable(obj) and not name.startswith('__'):
                    user_solution = obj
                    break
            
            if user_solution is None:
                return {
                    "success": False,
                    "error": "No function found in your solution."
                }
            
            # Run the verification
            results = self.verify_solution(user_solution)
            
            # Calculate time taken
            time_taken = time.time() - start_time
            results["time_taken"] = time_taken
            
            # Check if time limit exceeded (if there is one)
            if self.time_limit_seconds > 0 and time_taken > self.time_limit_seconds:
                results["success"] = False
                results["error"] = f"Time limit exceeded. Your solution took {time_taken:.2f}s, but the limit is {self.time_limit_seconds}s."
            
            # Update stats
            if results.get("success", False):
                self.times_completed += 1
                if time_taken < self.best_time:
                    self.best_time = time_taken
            
            return results
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error executing your solution: {str(e)}",
                "time_taken": time.time() - start_time
            }