import json
import os
import datetime
from typing import Dict, Optional
from src.game.character import Character, CharacterClass, Skill


class SaveManager:
    """Manages saving and loading game state."""

    def __init__(self, save_dir: str = "saves"):
        """Initialize the save manager."""
        self.save_dir = save_dir

        # Create the save directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def save_game(self, character: Character) -> bool:
        """
        Save the game state.

        Args:
            character: The player's character

        Returns:
            True if save was successful, False otherwise
        """
        try:
            save_data = {
                "name": character.name,
                "class": character.character_class.value,
                "level": character.level,
                "experience": character.experience,
                "challenges_completed": character.challenges_completed,
                "skills": {skill.name: level for skill, level in character.skills.items()},
                "inventory": character.inventory,
                "unlocked_areas": character.unlocked_areas,
                "timestamp": datetime.datetime.now().isoformat()
            }

            filename = f"{character.name.lower().replace(' ', '_')}.json"
            filepath = os.path.join(self.save_dir, filename)

            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=2)

            return True

        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, character_name: str) -> Optional[Character]:
        """
        Load a saved game.

        Args:
            character_name: Name of the character to load

        Returns:
            Loaded Character object, or None if load failed
        """
        try:
            filename = f"{character_name.lower().replace(' ', '_')}.json"
            filepath = os.path.join(self.save_dir, filename)

            if not os.path.exists(filepath):
                return None

            with open(filepath, 'r') as f:
                save_data = json.load(f)

            # Create character from save data
            character = Character(
                name=save_data["name"],
                character_class=CharacterClass(save_data["class"]),
                level=save_data["level"],
                experience=save_data["experience"],
                challenges_completed=save_data["challenges_completed"],
                inventory=save_data["inventory"],
                unlocked_areas=save_data["unlocked_areas"]
            )

            # Load skills
            character.skills = {
                Skill[skill_name]: level for skill_name, level in save_data["skills"].items()}

            return character

        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    def get_saved_games(self) -> Dict[str, str]:
        """
        Get a list of saved games.

        Returns:
            Dict mapping character names to timestamps
        """
        saved_games = {}

        for filename in os.listdir(self.save_dir):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(self.save_dir, filename), 'r') as f:
                        save_data = json.load(f)

                    saved_games[save_data["name"]] = save_data["timestamp"]

                except Exception:
                    # Skip corrupted save files
                    continue

        return saved_games
