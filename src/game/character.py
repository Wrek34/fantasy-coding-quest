from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


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
    name: str
    character_class: CharacterClass
    level: int = 1
    experience: int = 0
    challenges_completed: int = 0
    skills: Dict[Skill, int] = field(default_factory=dict)
    inventory: List[str] = field(default_factory=list)
    unlocked_areas: List[str] = field(default_factory=lambda: ["Algorithm Forest"])
    
    def __post_init__(self):
        # Initialize all skills with base values depending on character class
        for skill in Skill:
            self.skills[skill] = 1  # Base skill level
        
        # Boost skills based on character class
        if self.character_class == CharacterClass.ALGORITHM_WIZARD:
            self.skills[Skill.DYNAMIC_PROGRAMMING] = 2
            self.skills[Skill.RECURSION] = 2
        elif self.character_class == CharacterClass.DATA_STRUCTURE_PALADIN:
            self.skills[Skill.ARRAYS] = 2
            self.skills[Skill.LINKED_LISTS] = 2
            self.skills[Skill.TREES] = 2
        elif self.character_class == CharacterClass.DEBUGGING_ROGUE:
            self.skills[Skill.SEARCHING] = 2
            self.skills[Skill.SORTING] = 2
        elif self.character_class == CharacterClass.SYSTEM_DESIGN_DRUID:
            self.skills[Skill.SYSTEM_DESIGN] = 2
            self.skills[Skill.DATABASES] = 2
        elif self.character_class == CharacterClass.FULLSTACK_BARD:
            # Jack of all trades
            for skill in Skill:
                self.skills[skill] = 1.5
    
    def gain_experience(self, amount: int) -> bool:
        """Add experience points and handle level ups. Returns True if leveled up."""
        self.experience += amount
        
        # Check if level up (simple formula: 100 * current level to level up)
        xp_needed = 100 * self.level
        if self.experience >= xp_needed:
            self.experience -= xp_needed
            self.level += 1
            return True
        return False
    
    def complete_challenge(self, challenge_name: str, skill: Skill, xp_gained: int) -> None:
        """Record a completed challenge and gain experience and skill."""
        self.challenges_completed += 1
        leveled_up = self.gain_experience(xp_gained)
        
        # Improve the relevant skill
        self.skills[skill] = min(10, self.skills[skill] + 0.2)  # Cap skill at 10
        
        # If level is 5, 10, 15, etc., unlock a new area
        if self.level % 5 == 0 and self.level > 0:
            areas = ["Data Structure Mountains", "Database Dungeon", "System Design Citadel", 
                     "Web Development Shores", "Cloud Kingdom"]
            # Unlock a new area if there are any left to unlock
            for area in areas:
                if area not in self.unlocked_areas:
                    self.unlocked_areas.append(area)
                    break
    
    def add_to_inventory(self, item: str) -> None:
        """Add an item to the character's inventory."""
        self.inventory.append(item)
    
    def get_stats(self) -> Dict:
        """Return character stats as a dictionary."""
        return {
            "name": self.name,
            "class": self.character_class.value,
            "level": self.level,
            "experience": self.experience,
            "xp_to_next_level": 100 * self.level,
            "challenges_completed": self.challenges_completed,
            "skills": {skill.value: level for skill, level in self.skills.items()},
            "inventory": self.inventory,
            "unlocked_areas": self.unlocked_areas
        }