import pytest
from src.challenges.challenge_base import Challenge, DifficultyLevel, ChallengeType


class SimpleTestChallenge(Challenge):
    """A simple challenge for testing purposes."""

    def __init__(self):
        test_cases = [
            {
                "input": {"a": 1, "b": 2},
                "expected": 3
            },
            {
                "input": {"a": -1, "b": 1},
                "expected": 0
            }
        ]

        super().__init__(
            id="test-challenge",
            name="Test Challenge",
            description="A test challenge",
            difficulty=DifficultyLevel.EASY,
            challenge_type=ChallengeType.ALGORITHM,
            xp_reward=50,
            time_limit_seconds=30,
            test_cases=test_cases,
            hints=["Test hint"],
            solution="def add(a, b): return a + b",
            area="Algorithm Forest"
        )

    def verify_solution(self, user_solution):
        results = {
            "success": True,
            "test_cases": [],
            "time_taken": 0.1,
            "feedback": ["Good job!"]
        }

        for tc in self.test_cases:
            try:
                result = user_solution(**tc["input"])
                if result == tc["expected"]:
                    results["test_cases"].append({"passed": True})
                else:
                    results["success"] = False
                    results["test_cases"].append({
                        "passed": False,
                        "error": f"Expected {tc['expected']}, got {result}"
                    })
            except Exception as e:
                results["success"] = False
                results["test_cases"].append({
                    "passed": False,
                    "error": str(e)
                })

        return results


def test_challenge_attributes():
    """Test that a challenge has the expected attributes."""
    challenge = SimpleTestChallenge()

    assert challenge.id == "test-challenge"
    assert challenge.name == "Test Challenge"
    assert challenge.difficulty == DifficultyLevel.EASY
    assert challenge.challenge_type == ChallengeType.ALGORITHM
    assert challenge.xp_reward == 50
    assert challenge.area == "Algorithm Forest"


def test_challenge_solution_evaluation():
    """Test that a challenge can evaluate solutions correctly."""
    challenge = SimpleTestChallenge()

    # Test correct solution
    def correct_solution(a, b):
        return a + b

    result = challenge.attempt_solution(correct_solution)
    assert result["success"] is True

    # Test incorrect solution
    def incorrect_solution(a, b):
        return a - b

    result = challenge.attempt_solution(incorrect_solution)
    assert result["success"] is False
