import os
import importlib
import inspect
from typing import Dict, List, Any, Type
from src.challenges.challenge_base import Challenge


class ChallengeLoader:
    """Loads challenges from the challenges directory."""

    def __init__(self):
        """Initialize the challenge loader."""
        self.challenges = {}
        self.load_challenges()

    def load_challenges(self) -> None:
        """Load all challenge classes from the challenges directory."""
        # Base directory for challenges
        base_dir = os.path.dirname(os.path.abspath(__file__))
        challenges_dir = os.path.join(base_dir, "challenges")

        # Load algorithm challenges
        self._load_from_dir(os.path.join(challenges_dir, "algorithms"))

        # Future directories to load from:
        # self._load_from_dir(os.path.join(challenges_dir, "data_structures"))
        # self._load_from_dir(os.path.join(challenges_dir, "system_design"))
        # etc.

    def _load_from_dir(self, directory: str) -> None:
        """Load challenges from a specific directory."""
        if not os.path.exists(directory):
            return

        # Get Python files in the directory
        for filename in os.listdir(directory):
            if filename.endswith(".py") and not filename.startswith("__"):
                # Convert path to module name
                rel_path = os.path.relpath(directory, os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__))))
                module_path = f"src.{rel_path.replace(os.sep, '.')}.{filename[:-3]}"

                try:
                    # Import the module
                    module = importlib.import_module(module_path)

                    # Find challenge classes in the module
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and
                            issubclass(obj, Challenge) and
                                obj != Challenge):

                            # Instantiate the challenge
                            challenge = obj()
                            self.challenges[challenge.id] = challenge

                except Exception as e:
                    print(f"Error loading challenge from {filename}: {e}")

    def get_challenge(self, challenge_id: str) -> Challenge:
        """Get a challenge by ID."""
        return self.challenges.get(challenge_id)

    def get_challenges_by_area(self, area: str) -> List[Challenge]:
        """Get all challenges in a specific area."""
        return [c for c in self.challenges.values() if c.area == area]

    def get_all_challenges(self) -> Dict[str, Challenge]:
        """Get all loaded challenges."""
        return self.challenges
