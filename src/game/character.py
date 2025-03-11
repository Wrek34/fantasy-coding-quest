from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class CharacterClass(Enum):
    ALGORITHM_WIZARD = "Algorithm Wizard"
    DATA_STRUCTURE_PALADIN = "Data Structure Paladin"
    DEBUGGING_ROGUE = "Debugging Rogue"
    SYSTEM_DESIGN_DRUID = "System Design Druid"
    FULLSTACK_BARD = "Fullstack Bard"


class Skill(Enum):
    ARRAYS = "Arrays"
    LINKED_LISTS = "Linked Lists"
    TREES = "Trees"
    GRAPHS = "Graphs"
    DYNAMIC_PROGRAMMING = "Dynamic Programming"
    SORTING = "Sorting"
    SEARCHING = "Searching"
    RECURSION = "Recursion"
    DATABASES = "Databases"
    SYSTEM_DESIGN = "System Design"


@dataclass
class Character:
    """Represents a player character in the game."""

    def __init__(self, name: str, character_class: CharacterClass):
        """Initialize a character."""
        self.name = name
        self.character_class = character_class
        self.level = 1
        self.experience = 0
        self.xp_to_next_level = self.calculate_xp_for_level(
            2)  # XP needed for level 2
        # Start with level 1 in all skills
        self.skills = {skill.name: 1 for skill in Skill}
        self.completed_challenges = []
        # Start with the first area unlocked
        self.unlocked_areas = ["Algorithm Forest"]

    def calculate_xp_for_level(self, level: int) -> int:
        """
        Calculate XP required for a given level using a standard RPG formula.

        Args:
            level: The level to calculate XP for

        Returns:
            The amount of XP required to reach the level
        """
        # Using a common RPG leveling formula: 50 * level^2 - 150 * level + 200
        # This creates a curve where higher levels require more XP
        return int(50 * (level ** 2) - 150 * level + 200)

    def add_experience(self, amount: int) -> bool:
        """
        Add experience points to the character and check for level up.

        Args:
            amount: Amount of XP to add

        Returns:
            True if the character leveled up, False otherwise
        """
        old_level = self.level
        self.experience += amount

        # Check if we've reached the next level threshold
        leveled_up = False

        # Continue leveling up as long as we have enough XP
        while self.experience >= self.xp_to_next_level:
            self.level += 1
            self.experience -= self.xp_to_next_level
            self.xp_to_next_level = self.calculate_xp_for_level(self.level + 1)
            leveled_up = True

            # Check if new areas should be unlocked
            self._check_area_unlocks()

        return leveled_up

    def complete_challenge(self, challenge_name: str, skill: Optional[str] = None, xp_gained: int = 0) -> None:
        """
        Mark a challenge as completed and improve a skill if applicable.

        Args:
            challenge_name: Name of the completed challenge
            skill: Skill to improve (if any)
            xp_gained: XP gained from the challenge
        """
        if challenge_name not in self.completed_challenges:
            self.completed_challenges.append(challenge_name)

            # Improve the relevant skill if specified
            if skill and skill in self.skills:
                self.skills[skill] += 1

    def _check_area_unlocks(self) -> List[str]:
        """
        Check if new areas should be unlocked based on level.

        Returns:
            List of newly unlocked areas
        """
        new_areas = []

        # Define area unlock requirements
        area_unlocks = {
            "Data Structure Dungeon": 3,    # Unlocked at level 3
            "Function Fields": 5,           # Unlocked at level 5
            "Object-Oriented Oasis": 8,     # Unlocked at level 8
            "Recursive Ruins": 12,          # Unlocked at level 12
            "Debugging Desert": 15,         # Unlocked at level 15
            "Optimization Ocean": 20        # Unlocked at level 20
        }

        # Check each area
        for area, required_level in area_unlocks.items():
            if self.level >= required_level and area not in self.unlocked_areas:
                self.unlocked_areas.append(area)
                new_areas.append(area)

        return new_areas

    def get_stats(self) -> Dict[str, Any]:
        """
        Get the character's stats.

        Returns:
            Dictionary with character stats
        """
        return {
            "name": self.name,
            "class": self.character_class.value,
            "level": self.level,
            "experience": self.experience,
            "xp_to_next_level": self.xp_to_next_level,
            "skills": self.skills,
            "challenges_completed": len(self.completed_challenges),
            "unlocked_areas": self.unlocked_areas
        }
