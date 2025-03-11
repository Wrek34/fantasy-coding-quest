#!/usr/bin/env python3
import os
import sys
import inspect
import importlib
import pkgutil
import traceback


def check_dir_structure():
    """Check if required directories exist."""
    required_dirs = [
        "src",
        "src/game",
        "src/challenges",
        "src/challenges/challenges",
        "src/challenges/challenges/algorithms",
        "src/challenges/challenges/data_structures",
        "src/ai",
        "docs",
    ]
    
    missing_dirs = [d for d in required_dirs if not os.path.isdir(d)]
    if missing_dirs:
        print("❌ Missing directories:")
        for d in missing_dirs:
            print(f"  - {d}")
        print("Creating missing directories...")
        for d in missing_dirs:
            os.makedirs(d, exist_ok=True)
        print("✅ Created missing directories")
    else:
        print("✅ Directory structure looks good")
    
    return len(missing_dirs) == 0


def check_init_files():
    """Check if __init__.py files exist in all packages."""
    packages = [
        "src",
        "src/game",
        "src/challenges",
        "src/challenges/challenges",
        "src/challenges/challenges/algorithms",
        "src/challenges/challenges/data_structures",
        "src/ai",
    ]
    
    missing_inits = [f"{p}/__init__.py" for p in packages if not os.path.isfile(f"{p}/__init__.py")]
    if missing_inits:
        print("❌ Missing __init__.py files:")
        for f in missing_inits:
            print(f"  - {f}")
        print("Creating missing __init__.py files...")
        for f in missing_inits:
            with open(f, 'w') as file:
                file.write("# Package initialization\n")
        print("✅ Created missing __init__.py files")
    else:
        print("✅ All __init__.py files exist")
    
    return len(missing_inits) == 0


def check_ui_methods():
    """Check if the UI class has all required methods."""
    try:
        from src.game.ui import UI
        
        required_methods = [
            "clear_screen",
            "print_title",
            "print_subtitle",
            "print_info",
            "print_warning",
            "print_success",
            "print_error",
            "menu",
            "display_challenge",
            "code_editor",
            "display_solution_results",
        ]
        
        ui = UI()
        missing_methods = []
        
        for method in required_methods:
            if not hasattr(ui, method) or not callable(getattr(ui, method)):
                missing_methods.append(method)
        
        if "get_input" not in dir(ui) and "prompt" in dir(ui):
            print("❌ UI class has prompt() but not get_input()")
            print("Adding get_input() alias for prompt()...")
            
            # Create the UI class template with the missing method
            ui_file_path = "src/game/ui.py"
            with open(ui_file_path, 'r') as file:
                content = file.read()
            
            if "def get_input" not in content:
                # Add the get_input method before the class ends
                new_method = '\n    def get_input(self, message: str) -> str:\n        """Alias for prompt method."""\n        return self.prompt(message)\n'
                if "def prompt" in content:
                    # Add after the prompt method
                    content = content.replace("def prompt", "def prompt" + new_method, 1)
                else:
                    # Add at the end of the class
                    content = content.replace("class UI:", "class UI:" + new_method, 1)
                
                with open(ui_file_path, 'w') as file:
                    file.write(content)
                
                print("✅ Added get_input() method to UI class")
        
        if missing_methods:
            print(f"❌ UI class is missing required methods: {', '.join(missing_methods)}")
            return False
        else:
            print("✅ UI class has all required methods")
            return True
    
    except Exception as e:
        print(f"❌ Error checking UI methods: {str(e)}")
        traceback.print_exc()
        return False


def check_character_initialization():
    """Check for issues with character initialization in main.py."""
    try:
        main_file_path = "src/main.py"
        with open(main_file_path, 'r') as file:
            content = file.read()
        
        # Check if _create_character sets self.character
        if "def _create_character" in content and "self.character =" not in content.split("def _create_character")[1].split("def")[0]:
            print("❌ _create_character method does not set self.character")
            
            # Try to fix the method
            if "_create_character" in content:
                create_char_method = content.split("def _create_character")[1].split("def")[0]
                name_line_present = "name =" in create_char_method
                
                if name_line_present and "character_class" not in create_char_method:
                    # Add Character initialization after name input
                    fixed_method = create_char_method.replace(
                        "name = ", 
                        "name = ", 1
                    )
                    fixed_method = fixed_method.replace(
                        "input", 
                        "input\n        \n        # Initialize character\n        from src.game.character import Character, CharacterClass\n        self.character = Character(name=name, character_class=CharacterClass.ALGORITHM_WIZARD)", 1
                    )
                    content = content.replace(create_char_method, fixed_method)
                    
                    with open(main_file_path, 'w') as file:
                        file.write(content)
                    
                    print("✅ Fixed character initialization in _create_character method")
        
        # Check if main_loop has a character check
        if "def _main_loop" in content and "if self.character is None" not in content.split("def _main_loop")[1].split("def")[0]:
            print("❌ _main_loop method does not check if character is None")
            
            # Add character check at the beginning of _main_loop
            main_loop_start = content.split("def _main_loop")[1].split(":")[0] + ":"
            main_loop_body = content.split("def _main_loop")[1].split(":")[1].split("def")[0]
            
            # Add null check
            fixed_main_loop = main_loop_start + """
        # Ensure character is initialized
        if self.character is None:
            self.ui.print_error("No character found. Creating a new character.")
            self._create_character()
            if self.character is None:
                self.ui.print_error("Failed to create character. Returning to main menu.")
                return
    """ + main_loop_body
            
            content = content.replace(
                "def _main_loop" + main_loop_start + main_loop_body,
                "def _main_loop" + fixed_main_loop
            )
            
            with open(main_file_path, 'w') as file:
                file.write(content)
            
            print("✅ Added character null check to _main_loop method")
        
        # Check the flow in start method
        if "def start" in content:
            start_method = content.split("def start")[1].split("def")[0]
            
            if "_main_loop" in start_method and "_create_character" not in start_method:
                print("❌ start method calls _main_loop without ensuring character exists")
                
                # Fix the start method
                if 'choice == 0:' in start_method and '_main_loop' in start_method:
                    # Add character creation before main loop
                    fixed_start = start_method.replace(
                        'choice == 0:', 
                        'choice == 0:  # New Game\n            self._create_character()'
                    )
                    content = content.replace(start_method, fixed_start)
                    
                    with open(main_file_path, 'w') as file:
                        file.write(content)
                    
                    print("✅ Fixed start method to create character before main loop")
        
        return True
    
    except Exception as e:
        print(f"❌ Error checking character initialization: {str(e)}")
        traceback.print_exc()
        return False


def check_dependencies():
    """Check if required Python packages are installed."""
    required_packages = [
        "pyfiglet",
        "colorama",
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        for package in missing_packages:
            os.system(f"pip install {package}")
        
        print("✅ Installed missing packages")
    else:
        print("✅ All required packages are installed")
    
    return len(missing_packages) == 0


def create_basic_character_class():
    """Create a basic Character class if it doesn't exist."""
    file_path = "src/game/character.py"
    
    if not os.path.exists(file_path):
        print("❌ Character class file is missing")
        print("Creating basic Character class...")
        
        from enum import Enum
        
        # Create the file content
        content = """from enum import Enum
from typing import Dict, List, Optional, Any


class CharacterClass(Enum):
    ALGORITHM_WIZARD = "Algorithm Wizard"
    DATA_RANGER = "Data Ranger"
    DEBUGGING_KNIGHT = "Debugging Knight"


class Skill(Enum):
    ARRAYS = "Arrays"
    LINKED_LISTS = "Linked Lists"
    TREES = "Trees"
    GRAPHS = "Graphs"
    SORTING = "Sorting"
    SEARCHING = "Searching"
    DYNAMIC_PROGRAMMING = "Dynamic Programming"
    RECURSION = "Recursion"


class Character:
    \"\"\"Represents a player character in the game.\"\"\"
    
    def __init__(self, name: str, character_class: CharacterClass):
        \"\"\"Initialize a new character.\"\"\"
        self.name = name
        self.character_class = character_class
        self.level = 1
        self.experience = 0
        self.skills = {skill: 1 for skill in Skill}  # All skills start at level 1
        self.inventory = []
        self.challenges_completed = 0
        self.unlocked_areas = ["Algorithm Forest"]  # First area unlocked by default
        
        # Apply class bonuses
        if character_class == CharacterClass.ALGORITHM_WIZARD:
            self.skills[Skill.ARRAYS] = 2
            self.skills[Skill.SORTING] = 2
        elif character_class == CharacterClass.DATA_RANGER:
            self.skills[Skill.LINKED_LISTS] = 2
            self.skills[Skill.TREES] = 2
        elif character_class == CharacterClass.DEBUGGING_KNIGHT:
            self.skills[Skill.RECURSION] = 2
            self.skills[Skill.DYNAMIC_PROGRAMMING] = 2
    
    def add_experience(self, xp: int) -> int:
        \"\"\"
        Add experience points to the character.
        
        Args:
            xp: Amount of XP to add
            
        Returns:
            New level if leveled up, 0 otherwise
        \"\"\"
        self.experience += xp
        
        # Check for level up
        xp_to_next_level = self.xp_to_next_level()
        
        if self.experience >= xp_to_next_level:
            self.experience -= xp_to_next_level
            self.level += 1
            return self.level
        
        return 0
    
    def xp_to_next_level(self) -> int:
        \"\"\"Calculate XP needed for next level.\"\"\"
        return self.level * 100
    
    def complete_challenge(self, challenge_name: str, skill: Optional[Skill] = None, xp_gained: int = 0) -> None:
        \"\"\"
        Mark a challenge as completed and improve relevant skill.
        
        Args:
            challenge_name: Name of the completed challenge
            skill: Primary skill used in the challenge
            xp_gained: XP earned from the challenge
        \"\"\"
        self.challenges_completed += 1
        
        if skill and skill in self.skills:
            # Improve the skill slightly
            self.skills[skill] += 0.1
    
    def get_stats(self) -> Dict[str, Any]:
        \"\"\"Get character statistics as a dictionary.\"\"\"
        return {
            "name": self.name,
            "class": self.character_class.value,
            "level": self.level,
            "experience": self.experience,
            "xp_to_next_level": self.xp_to_next_level(),
            "skills": {skill.value: round(level, 1) for skill, level in self.skills.items()},
            "challenges_completed": self.challenges_completed,
            "unlocked_areas": self.unlocked_areas
        }
    
    def check_level_up(self) -> int:
        \"\"\"Check if character has leveled up.\"\"\"
        if self.experience >= self.xp_to_next_level():
            old_level = self.level
            self.level += 1
            self.experience -= self.xp_to_next_level()
            return self.level
        return 0
    
    def check_area_unlocks(self) -> List[str]:
        \"\"\"Check if new areas should be unlocked based on level.\"\"\"
        new_areas = []
        
        # Area unlock levels
        area_unlocks = {
            5: "Data Structure Mountains",
            10: "Algorithm Valley",
            15: "Debugging Desert",
            20: "Dynamic Programming Peaks"
        }
        
        for level, area in area_unlocks.items():
            if self.level >= level and area not in self.unlocked_areas:
                self.unlocked_areas.append(area)
                new_areas.append(area)
        
        return new_areas
"""
        
        # Write to file
        with open(file_path, 'w') as file:
            file.write(content)
        
        print("✅ Created basic Character class")
        return True
    
    print("✅ Character class file exists")
    return True


def create_basic_world_class():
    """Create a basic World class if it doesn't exist."""
    file_path = "src/game/world.py"
    
    if not os.path.exists(file_path):
        print("❌ World class file is missing")
        print("Creating basic World class...")
        
        content = """from enum import Enum


class Area(Enum):
    \"\"\"Represents a game area.\"\"\"
    ALGORITHM_FOREST = "Algorithm Forest"
    DATA_STRUCTURE_MOUNTAINS = "Data Structure Mountains"
    ALGORITHM_VALLEY = "Algorithm Valley"
    DEBUGGING_DESERT = "Debugging Desert"
    DYNAMIC_PROGRAMMING_PEAKS = "Dynamic Programming Peaks"


class World:
    \"\"\"Represents the game world.\"\"\"
    
    def __init__(self):
        \"\"\"Initialize the world.\"\"\"
        self.areas = {
            Area.ALGORITHM_FOREST: {
                "level_required": 1,
                "description": "A peaceful forest where algorithm basics flourish."
            },
            Area.DATA_STRUCTURE_MOUNTAINS: {
                "level_required": 5,
                "description": "Majestic mountains where complex data structures are formed."
            },
            Area.ALGORITHM_VALLEY: {
                "level_required": 10,
                "description": "A valley where advanced algorithms flow like rivers."
            },
            Area.DEBUGGING_DESERT: {
                "level_required": 15,
                "description": "A harsh desert where bugs are hunted and eliminated."
            },
            Area.DYNAMIC_PROGRAMMING_PEAKS: {
                "level_required": 20,
                "description": "The highest peaks where mastery of dynamic programming is achieved."
            }
        }
    
    def get_areas(self):
        \"\"\"Get all areas in the world.\"\"\"
        return self.areas
    
    def get_area_description(self, area: Area) -> str:
        \"\"\"Get the description of an area.\"\"\"
        if area in self.areas:
            return self.areas[area]["description"]
        return "Unknown area"
    
    def get_area_level_requirement(self, area: Area) -> int:
        \"\"\"Get the level required to access an area.\"\"\"
        if area in self.areas:
            return self.areas[area]["level_required"]
        return 999  # Very high level for unknown areas
"""
        
        # Write to file
        with open(file_path, 'w') as file:
            file.write(content)
        
        print("✅ Created basic World class")
        return True
    
    print("✅ World class file exists")
    return True


def create_basic_save_manager():
    """Create a basic SaveManager class if it doesn't exist."""
    file_path = "src/game/save_manager.py"
    
    if not os.path.exists(file_path):
        print("❌ SaveManager class file is missing")
        print("Creating basic SaveManager class...")
        
        content = """import os
import json
import pickle
from typing import Optional, Dict, Any, List
from src.game.character import Character, CharacterClass, Skill


class SaveManager:
    \"\"\"Handles saving and loading game data.\"\"\"
    
    def __init__(self, save_dir: str = "saves"):
        \"\"\"Initialize the save manager.\"\"\"
        self.save_dir = save_dir
        
        # Create save directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def save_game(self, character: Character, additional_data: Dict[str, Any] = None) -> bool:
        \"\"\"
        Save the game state.
        
        Args:
            character: The character to save
            additional_data: Any additional data to save
            
        Returns:
            True if successful, False otherwise
        \"\"\"
        if not character:
            return False
        
        try:
            # Create a save data structure
            save_data = {
                "character": {
                    "name": character.name,
                    "class": character.character_class.value,
                    "level": character.level,
                    "experience": character.experience,
                    "skills": {skill.value: level for skill, level in character.skills.items()},
                    "inventory": character.inventory,
                    "challenges_completed": character.challenges_completed,
                    "unlocked_areas": character.unlocked_areas
                }
            }
            
            # Add any additional data
            if additional_data:
                save_data.update(additional_data)
            
            # Save to file
            save_path = os.path.join(self.save_dir, f"{character.name.lower()}.json")
            with open(save_path, 'w') as f:
                json.dump(save_data, f, indent=4)
            
            return True
        
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self, character_name: str) -> Optional[Character]:
        \"\"\"
        Load a saved game.
        
        Args:
            character_name: Name of the character to load
            
        Returns:
            Loaded Character or None if load failed
        \"\"\"
        try:
            save_path = os.path.join(self.save_dir, f"{character_name.lower()}.json")
            
            if not os.path.exists(save_path):
                return None
            
            with open(save_path, 'r') as f:
                save_data = json.load(f)
            
            # Extract character data
            char_data = save_data["character"]
            
            # Create a new character
            character = Character(
                name=char_data["name"],
                character_class=self._get_class_from_string(char_data["class"])
            )
            
            # Restore character state
            character.level = char_data["level"]
            character.experience = char_data["experience"]
            character.inventory = char_data["inventory"]
            character.challenges_completed = char_data["challenges_completed"]
            character.unlocked_areas = char_data["unlocked_areas"]
            
            # Restore skills
            for skill_name, level in char_data["skills"].items():
                for skill_enum in Skill:
                    if skill_enum.value == skill_name:
                        character.skills[skill_enum] = level
                        break
            
            return character
        
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    
    def get_saved_games(self) -> List[Dict[str, Any]]:
        \"\"\"
        Get a list of saved games.
        
        Returns:
            List of dictionaries with saved game info
        \"\"\"
        saved_games = []
        
        # Check if save directory exists
        if not os.path.exists(self.save_dir):
            return saved_games
        
        # Look for save files
        for filename in os.listdir(self.save_dir):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(self.save_dir, filename), 'r') as f:
                        save_data = json.load(f)
                    
                    char_data = save_data["character"]
                    saved_games.append({
                        "name": char_data["name"],
                        "class": char_data["class"],
                        "level": char_data["level"],
                        "filename": filename
                    })
                except:
                    # Skip invalid files
                    pass
        
        return saved_games
    
    def _get_class_from_string(self, class_str: str) -> CharacterClass:
        \"\"\"Convert a string to a CharacterClass enum.\"\"\"
        for char_class in CharacterClass:
            if char_class.value == class_str:
                return char_class
        
        # Default to Algorithm Wizard if not found
        return CharacterClass.ALGORITHM_WIZARD
"""
        
        # Write to file
        with open(file_path, 'w') as file:
            file.write(content)
        
        print("✅ Created basic SaveManager class")
        return True
    
    print("✅ SaveManager class file exists")
    return True


def create_base_challenge_files():
    """Create base challenge files if they don't exist."""
    # Create challenge_base.py
    base_file_path = "src/challenges/challenge_base.py"
    if not os.path.exists(base_file_path):
        print("❌ Challenge base class file is missing")
        print("Creating basic Challenge base class...")
        
        content = """from enum import Enum
from typing import List, Dict, Any, Callable, Optional


class DifficultyLevel(Enum):
    \"\"\"Enum for challenge difficulty levels.\"\"\"
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    EXPERT = "Expert"


class ChallengeType(Enum):
    \"\"\"Enum for challenge types.\"\"\"
    ALGORITHM = "Algorithm"
    DATA_STRUCTURE = "Data Structure"
    PATTERN = "Design Pattern"
    DEBUG = "Debugging"


class Challenge:
    \"\"\"Base class for all challenges.\"\"\"
    
    def __init__(
            self,
            id: str,
            name: str,
            description: str,
            difficulty: DifficultyLevel,
            challenge_type: ChallengeType,
            xp_reward: int,
            time_limit_seconds: int,
            test_cases: List[Dict[str, Any]],
            hints: List[str],
            solution: str,
            area: str,
            primary_skill: Any = None
        ):
        \"\"\"Initialize a challenge.\"\"\"
        self.id = id
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.challenge_type = challenge_type
        self.xp_reward = xp_reward
        self.time_limit_seconds = time_limit_seconds
        self.test_cases = test_cases
        self.hints = hints
        self.solution = solution
        self.area = area
        self.primary_skill = primary_skill
    
    def attempt_solution(self, user_solution: Callable) -> Dict[str, Any]:
        \"\"\"
        Evaluate a user's solution against the test cases.
        
        Args:
            user_solution: The user's solution function
            
        Returns:
            Dictionary with evaluation results
        \"\"\"
        return self.verify_solution(user_solution)
    
    def verify_solution(self, user_solution: Callable) -> Dict[str, Any]:
        \"\"\"
        Verify a solution against test cases.
        
        Args:
            user_solution: User's solution function
            
        Returns:
            Dict with verification results
        \"\"\"
        # This is implemented by subclasses
        results = {
            "success": True,
            "test_cases": [],
            "time_taken": 0,
            "feedback": []
        }
        
        return results
"""
        
        # Write to file
        with open(base_file_path, 'w') as file:
            file.write(content)
        
        print("✅ Created Challenge base class")
    
    # Create challenge_loader.py
    loader_file_path = "src/challenges/challenge_loader.py"
    if not os.path.exists(loader_file_path):
        print("❌ ChallengeLoader class file is missing")
        print("Creating basic ChallengeLoader class...")
        
        content = """import os
import importlib
import pkgutil
from typing import Dict, Any
from src.challenges.challenge_base import Challenge


class ChallengeLoader:
    \"\"\"Loads challenge classes dynamically.\"\"\"
    
    def __init__(self):
        \"\"\"Initialize the challenge loader.\"\"\"
        self.challenges_path = "src.challenges.challenges"
        self.challenges = {}
    
    def get_all_challenges(self) -> Dict[str, Challenge]:
        \"\"\"
        Load all challenge classes from the challenges directory.
        
        Returns:
            Dictionary of challenge ID to challenge instance
        \"\"\"
        if self.challenges:
            return self.challenges
        
        try:
            # Import the challenges package
            challenges_package = importlib.import_module(self.challenges_path)
            
            # Recursively discover subpackages (algorithms, data_structures, etc.)
            for _, name, is_pkg in pkgutil.iter_modules(challenges_package.__path__, challenges_package.__name__ + '.'):
                if is_pkg:
                    # This is a subpackage (like algorithms, data_structures)
                    subpackage = importlib.import_module(name)
                    
                    # Find all modules in this subpackage
                    for _, module_name, _ in pkgutil.iter_modules(subpackage.__path__, subpackage.__name__ + '.'):
                        try:
                            # Import the module
                            module = importlib.import_module(module_name)
                            
                            # Find all classes in the module
                            for attr_name in dir(module):
                                attr = getattr(module, attr_name)
                                
                                # Check if it's a Challenge subclass (not the Challenge class itself)
                                if (isinstance(attr, type) and 
                                    issubclass(attr, Challenge) and 
                                    attr is not Challenge and 
                                    attr.__name__.endswith('Challenge')):
                                    
                                    # Instantiate the challenge
                                    challenge = attr()
                                    
                                    # Add to dictionary
                                    self.challenges[challenge.id] = challenge
                        except Exception as e:
                            print(f"Error loading module {module_name}: {e}")
        except Exception as e:
            print(f"Error loading challenges: {e}")
            
            # Fallback - use manually created challenges
            try:
                from src.challenges.challenges.algorithms.two_sum import TwoSumChallenge
                challenge = TwoSumChallenge()
                self.challenges[challenge.id] = challenge
                
                # Try to load a linked_list_cycle challenge
                try:
                    from src.challenges.challenges.data_structures.linked_list_cycle import LinkedListCycleChallenge
                    challenge = LinkedListCycleChallenge()
                    self.challenges[challenge.id] = challenge
                except:
                    pass
                
                # Try to load a max_stack challenge  
                try:
                    from src.challenges.challenges.data_structures.max_stack import MaxStackChallenge
                    challenge = MaxStackChallenge()
                    self.challenges[challenge.id] = challenge
                except:
                    pass
            except:
                # Create a simple default challenge
                from src.challenges.challenge_base import Challenge, DifficultyLevel, ChallengeType
                
                class DefaultChallenge(Challenge):
                    def __init__(self):
                        super().__init__(
                            id="default-challenge",
                            name="Hello World",
                            description="Write a function hello() that returns 'Hello, World!'",
                            difficulty=DifficultyLevel.EASY,
                            challenge_type=ChallengeType.ALGORITHM,
                            xp_reward=10,
                            time_limit_seconds=60,
                            test_cases=[{"input": {}, "expected": "Hello, World!"}],
                            hints=["Just return the string 'Hello, World!'"],
                            solution="def hello():\\n    return 'Hello, World!'",
                            area="Algorithm Forest"
                        )
                    
                    def verify_solution(self, user_solution):
                        try:
                            result = user_solution()
                            success = result == "Hello, World!"
                            
                            return {
                                "success": success,
                                "test_cases": [{"passed": success}],
                                "time_taken": 0.1,
                                "feedback": ["Good job!"] if success else ["Try returning exactly 'Hello, World!'"]
                            }
                        except:
                            return {
                                "success": False,
                                "test_cases": [{"passed": False}],
                                "time_taken": 0.1,
                                "feedback": ["An error occurred when running your code."]
                            }
                
                challenge = DefaultChallenge()
                self.challenges[challenge.id] = challenge
        
        return self.challenges
    
    def get_challenge(self, challenge_id: str) -> Challenge:
        \"\"\"
        Get a specific challenge by ID.
        
        Args:
            challenge_id: ID of the challenge to get
            
        Returns:
            Challenge instance or None if not found
        \"\"\"
        if not self.challenges:
            self.get_all_challenges()
        
        return self.challenges.get(challenge_id, None)
"""
        
        # Write to file
        with open(loader_file_path, 'w') as file:
            file.write(content)
        
        print("✅ Created ChallengeLoader class")
    
    # Create a simple challenge
    default_challenge_dir = "src/challenges/challenges/algorithms"
    if not os.path.exists(default_challenge_dir):
        os.makedirs(default_challenge_dir, exist_ok=True)
    
    default_challenge_path = f"{default_challenge_dir}/two_sum.py"
    if not os.path.exists(default_challenge_path):
        print("❌ No sample challenge found")
        print("Creating a simple TwoSum challenge...")
        
        content = """import time
from typing import List, Dict, Any, Callable
from src.challenges.challenge_base import Challenge, DifficultyLevel, ChallengeType


class TwoSumChallenge(Challenge):
    \"\"\"
    A simple two sum challenge.
    \"\"\"
    
    def __init__(self):
        description = \"\"\"
        In the Algorithm Forest, you encounter a puzzle at a crossroads.
        
        You are given an array of integers and a target sum. You must find two numbers in the array
        that add up to the target sum and return their indices.
        
        Write a function called 'two_sum' that accepts:
        - nums: A list of integers
        - target: An integer
        
        Your function should return:
        - A list of two integers representing the indices of the two numbers in the array
          that add up to the target sum.
        
        Assume:
        - Each input has exactly one solution
        - You may not use the same element twice
        - You can return the answer in any order
        
        Example:
        - Input: nums = [2, 7, 11, 15], target = 9
        - Output: [0, 1] (because nums[0] + nums[1] = 2 + 7 = 9)
        \"\"\"
        
        hints = [
            "Consider using a hash map to store numbers you've seen and their indices.",
            "For each number, check if the target minus the current number exists in your hash map.",
            "Be careful not to use the same element twice!"
        ]
        
        solution = \"\"\"
        def two_sum(nums, target):
            # Create a hashmap to store numbers and their indices
            seen = {}
            
            # Iterate through the array
            for i, num in enumerate(nums):
                # Calculate the complement
                complement = target - num
                
                # Check if complement exists in our hashmap
                if complement in seen:
                    # Return the indices of the two numbers
                    return [seen[complement], i]
                
                # Add current number and its index to hashmap
                seen[num] = i
            
            # No solution found (though problem states there is always a solution)
            return []
        \"\"\"
        
        test_cases = [
            {
                "input": {"nums": [2, 7, 11, 15], "target": 9},
                "expected": [0, 1]
            },
            {
                "input": {"nums": [3, 2, 4], "target": 6},
                "expected": [1, 2]
            },
            {
                "input": {"nums": [3, 3], "target": 6},
                "expected": [0, 1]
            },
            {
                "input": {"nums": [1, 2, 3, 4, 5], "target": 9},
                "expected": [3, 4]
            }
        ]
        
        super().__init__(
            id="two-sum",
            name="The Two Sum Spell",
            description=description,
            difficulty=DifficultyLevel.EASY,
            challenge_type=ChallengeType.ALGORITHM,
            xp_reward=50,
            time_limit_seconds=120,
            test_cases=test_cases,
            hints=hints,
            solution=solution,
            area="Algorithm Forest"
        )
    
    def verify_solution(self, user_solution: Callable) -> Dict[str, Any]:
        \"\"\"
        Run test cases against the user's solution.
        
        Args:
            user_solution: User's solution function
            
        Returns:
            Dict with verification results
        \"\"\"
        results = {
            "success": True,
            "test_cases": [],
            "time_taken": 0,
            "feedback": []
        }
        
        start_time = time.time()
        
        for tc in self.test_cases:
            try:
                input_data = tc["input"]
                expected = tc["expected"]
                
                # Call the user's solution
                user_result = user_solution(**input_data)
                
                # Sort both results for comparison (since order doesn't matter)
                user_result = sorted(user_result) if user_result else user_result
                expected_sorted = sorted(expected)
                
                # Check if the result is correct
                passed = user_result == expected_sorted
                
                test_result = {
                    "passed": passed,
                    "input": input_data,
                    "expected": expected,
                    "actual": user_result
                }
                
                if not passed:
                    results["success"] = False
                    test_result["error"] = f"Expected {expected_sorted}, got {user_result}"
                
                results["test_cases"].append(test_result)
                
            except Exception as e:
                results["success"] = False
                results["test_cases"].append({
                    "passed": False,
                    "input": tc["input"],
                    "expected": tc["expected"],
                    "error": str(e)
                })
        
        results["time_taken"] = time.time() - start_time 