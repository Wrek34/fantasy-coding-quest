# Development Guide for Fantasy Coding Quest

This guide is intended for developers who want to contribute to the Fantasy Coding Quest project.

## Project Architecture

Fantasy Coding Quest follows a modular architecture:

```
fantasy-coding-quest/
├── src/                      # Source code
│   ├── ai/                   # AI-related functionality
│   │   ├── hint_generator.py # Generates hints for challenges
│   │   ├── solution_evaluator.py # Evaluates user solutions
│   │   └── ...
│   ├── challenges/           # Challenge definitions
│   │   ├── challenge_base.py # Base challenge class
│   │   ├── challenge_loader.py # Loads challenges dynamically
│   │   ├── challenges/       # Challenge implementations
│   │   │   ├── algorithms/   # Algorithm challenges
│   │   │   ├── data_structures/ # Data structure challenges
│   │   │   └── ...
│   ├── game/                 # Game mechanics
│   │   ├── character.py      # Character system
│   │   ├── world.py         # World and area definitions
│   │   ├── ui.py            # User interface
│   │   └── ...
│   └── main.py              # Main entry point
├── docs/                    # Documentation
├── tests/                   # Test suite
└── requirements.txt         # Dependencies
```

## Development Setup

1. Clone the repository:

```bash
git clone https://github.com/wrek34/fantasy-coding-quest.git
cd fantasy-coding-quest
```

2. Create and activate a virtual environment:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install development dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If you create this file with dev dependencies
```

4. Run tests to ensure everything is working:

```bash
pytest
```

## Adding New Challenges

To add a new challenge:

1. Determine the appropriate category (algorithms, data structures, etc.)
2. Create a new Python file in the corresponding directory under `src/challenges/challenges/`
3. Define a class that inherits from `Challenge`
4. Implement the required methods and attributes
5. Your challenge class should have:
   - A descriptive fantasy-themed problem statement
   - Test cases with inputs and expected outputs
   - Hints for players who get stuck
   - A solution for reference

Example:

```python
class MyNewChallenge(Challenge):
    def __init__(self):
        description = """
        Fantasy-themed problem description goes here...
        """

        hints = [
            "First hint - very general",
            "Second hint - more specific",
            "Third hint - almost gives away the solution"
        ]

        solution = """
        def my_solution(param1, param2):
            # Solution code here
            return result
        """

        test_cases = [
            {
                "input": {"param1": value1, "param2": value2},
                "expected": expected_output
            },
            # More test cases...
        ]

        super().__init__(
            id="unique-challenge-id",
            name="Fantasy Name for the Challenge",
            description=description,
            difficulty=DifficultyLevel.MEDIUM,  # Choose appropriate difficulty
            challenge_type=ChallengeType.ALGORITHM,  # Choose appropriate type
            xp_reward=75,  # XP reward based on difficulty
            time_limit_seconds=45,  # Optional time limit
            test_cases=test_cases,
            hints=hints,
            solution=solution,
            area="Algorithm Forest"  # Area in the game world
        )

    def verify_solution(self, user_solution):
        # Implement verification logic
        # Usually uses the SolutionEvaluator
        from src.ai.solution_evaluator import SolutionEvaluator

        evaluator = SolutionEvaluator()
        return evaluator.evaluate(
            solution_func=user_solution,
            test_cases=self.test_cases,
            expected_time_complexity="O(n)",
            expected_space_complexity="O(1)"
        )
```

## Adding New Game Areas

To add a new area to the game world:

1. Add the area to the `Area` enum in `src/game/world.py`
2. Add the area details to the `areas` dictionary in the `World` class constructor
3. Create new challenges for the area

## Improving the AI Components

The AI components in `src/ai/` can be enhanced:

1. `hint_generator.py`: Improve hint generation with more advanced techniques or integration with AI models
2. `solution_evaluator.py`: Add more sophisticated code analysis
3. Add new AI components for features like personalized learning paths

## Running Tests

Tests are organized in the `tests/` directory. To run tests:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_character.py

# Run with verbose output
pytest -v
```

## Code Style

This project follows PEP 8 style guidelines. You can use tools like:

```bash
# Install development tools
pip install black flake8

# Format code
black src/

# Check for style issues
flake8 src/
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request with a clear description of the changes

## Contact

If you have questions about development, please open an issue on GitHub.
