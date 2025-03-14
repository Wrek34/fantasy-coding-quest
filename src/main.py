#!/usr/bin/env python3
import sys
import os
import random
from typing import List, Optional

from src.game.character import Character, CharacterClass, Skill
from src.game.world import World, Area
from src.game.ui import UI
from src.game.save_manager import SaveManager
from src.challenges.challenge_base import Challenge, DifficultyLevel, ChallengeType


class Game:
    """Main game class for Fantasy Coding Quest."""

    def __init__(self):
        """Initialize the game components."""
        self.ui = UI()
        self.world = World()
        self.character = None
        self.save_manager = SaveManager()

        # Load challenges
        self.challenges = self._load_challenges()

    def _load_challenges(self):
        """Load all challenges (placeholder for dynamic loading)."""
        # In a future version, this will use ChallengeLoader to load dynamically
        from src.challenges.challenges.algorithms.two_sum import TwoSumChallenge

        # For now, manually create and return challenges
        challenges = {
            "two-sum": TwoSumChallenge()
        }

        # Add beginner challenges if they exist
        try:
            from src.challenges.challenges.algorithms.hello_world import HelloWorldChallenge
            challenges["hello-world"] = HelloWorldChallenge()
        except ImportError:
            pass

        try:
            from src.challenges.challenges.algorithms.sum_of_two import SumOfTwoChallenge
            challenges["sum-of-two"] = SumOfTwoChallenge()
        except ImportError:
            pass

        # Try to load data structure challenges
        try:
            from src.challenges.challenges.data_structures.linked_list_cycle import LinkedListCycleChallenge
            challenges["linked-list-cycle"] = LinkedListCycleChallenge()
        except ImportError:
            pass

        try:
            from src.challenges.challenges.data_structures.max_stack import MaxStackChallenge
            challenges["max-stack"] = MaxStackChallenge()
        except ImportError:
            pass

        return challenges

    def start(self):
        """Start the game."""
        self.ui.clear_screen()
        self.ui.print_title("Fantasy Coding Quest")

        # Check if returning player or new
        choice = self.ui.menu("Welcome, adventurer!", [
                              "New Game", "Load Game", "Tutorial", "Exit"])

        if choice == 0:  # New Game
            success = self._create_character()
            if success and self.character is not None:
                self._main_loop()
            else:
                self.ui.print_error(
                    "Failed to create character. Please try again.")
                input("\nPress Enter to continue...")
                self.start()  # Return to main menu
        elif choice == 1:  # Load Game
            self._load_game()
        elif choice == 2:  # Tutorial
            self._show_tutorial()
            self.start()  # Return to main menu after tutorial
        else:
            sys.exit(0)

    def _create_character(self):
        """Create a new character."""
        try:
            self.ui.clear_screen()
            self.ui.print_subtitle("Character Creation")

            # Get character name
            try:
                # First try prompt if it exists
                name = self.ui.prompt("What is your name, adventurer?")
            except AttributeError:
                # Fall back to get_input if prompt doesn't exist
                name = self.ui.get_input("What is your name, adventurer?")

            if not name.strip():
                name = "Adventurer"  # Default name if empty

            # Get character class
            self.ui.print_subtitle("Choose Your Class")

            class_options = []
            for char_class in CharacterClass:
                class_options.append(f"{char_class.value}")

            class_choice = self.ui.menu("Select your class:", class_options)
            selected_class = list(CharacterClass)[class_choice]

            # Create the character
            self.character = Character(
                name=name, character_class=selected_class)

            self.ui.clear_screen()
            self.ui.print_success(
                f"Welcome, {name} the {selected_class.value}!")
            self.ui.print_info(
                "Your adventure begins in the Algorithm Forest, where you'll face your first coding challenges.")
            input("\nPress Enter to continue...")

            return True
        except Exception as e:
            self.ui.print_error(f"Error creating character: {str(e)}")
            return False

    def _load_game(self):
        """Load a saved game."""
        saved_games = self.save_manager.get_saved_games()

        if not saved_games:
            self.ui.print_warning("No saved games found.")
            input("Press Enter to continue...")
            self.start()
            return

        # Create a menu of saved games
        options = list(saved_games.keys())
        options.append("Return to Main Menu")

        self.ui.clear_screen()
        self.ui.print_subtitle("Load Game")

        choice = self.ui.menu("Select a saved game:", options)

        if choice < len(saved_games):
            character_name = options[choice]
            self.character = self.save_manager.load_game(character_name)

            if self.character:
                self.ui.print_success(f"Welcome back, {self.character.name}!")
                input("\nPress Enter to continue...")
                self._main_loop()
            else:
                self.ui.print_error(
                    f"Failed to load game for {character_name}.")
                input("\nPress Enter to continue...")
                self.start()
        else:
            self.start()  # Return to main menu

    def _main_loop(self):
        """Main game loop."""
        while True:
            self.ui.clear_screen()
            self.ui.print_subtitle(
                f"Character: {self.character.name} (Level {self.character.level})")

            # Display character info
            self.ui.print_info(
                f"Class: {self.character.character_class.value}")
            self.ui.print_info(
                f"XP: {self.character.experience}/{100 * self.character.level} to next level")
            self.ui.print_info(
                f"Challenges Completed: {self.character.challenges_completed}")

            # Main menu options
            choice = self.ui.menu("What would you like to do?", [
                "Take on a Challenge",
                "View Map",
                "View Character",
                "Save Game",
                "Exit to Main Menu"
            ])

            if choice == 0:  # Challenge
                self._select_challenge()
            elif choice == 1:  # Map
                self._show_map()
            elif choice == 2:  # Character
                self._view_character()
            elif choice == 3:  # Save
                if self.save_manager.save_game(self.character):
                    self.ui.print_success("Game saved successfully!")
                else:
                    self.ui.print_error("Failed to save game.")
                input("\nPress Enter to continue...")
            else:
                if self.ui.confirm("Are you sure you want to exit? Unsaved progress will be lost."):
                    break

    def _show_map(self):
        """Display the world map."""
        self.ui.clear_screen()
        self.ui.print_subtitle("World Map")

        # Get unlocked and locked areas
        unlocked = self.character.unlocked_areas
        all_areas = [area.value for area in Area]
        locked = [area for area in all_areas if area not in unlocked]

        # Display the map
        self.ui.print_info(self.world.display_map())

        # Show unlocked areas
        self.ui.print_subtitle("Unlocked Areas:")
        for area in unlocked:
            self.ui.print_success(f"✓ {area}")

        # Show locked areas
        if locked:
            self.ui.print_subtitle("Locked Areas:")
            for area in locked:
                self.ui.print_warning(
                    f"🔒 {area} (Reach higher levels to unlock)")

        input("\nPress Enter to continue...")

    def _select_challenge(self):
        """Select a challenge to attempt."""
        self.ui.clear_screen()
        self.ui.print_subtitle("Available Challenges")

        # Get current area
        # Default to first area
        current_area = self.character.unlocked_areas[0]

        # Get challenges for this area
        area_challenges = [
            c for c in self.challenges.values() if c.area == current_area]

        if not area_challenges:
            self.ui.print_warning(
                f"No challenges available in {current_area} yet.")
            input("\nPress Enter to return...")
            return

        # Create a menu of challenges
        challenge_options = [
            f"{c.name} - {c.difficulty.value} ({c.xp_reward} XP)" for c in area_challenges]
        challenge_options.append("Return to Main Menu")

        choice = self.ui.menu("Select a challenge:", challenge_options)

        if choice >= len(area_challenges):
            return  # Return to main menu

        # Get the selected challenge
        selected_challenge = area_challenges[choice]

        self.ui.display_challenge({
            "name": selected_challenge.name,
            "area": selected_challenge.area,
            "difficulty": selected_challenge.difficulty.value,
            "challenge_type": selected_challenge.challenge_type.value,
            "xp_reward": selected_challenge.xp_reward,
            "time_limit_seconds": selected_challenge.time_limit_seconds,
            "description": selected_challenge.description
        })

        choice = self.ui.menu("What would you like to do?", [
            "Attempt Challenge",
            "Get a Hint",
            "Return to Main Menu"
        ])

        if choice == 0:  # Attempt
            self._attempt_challenge(selected_challenge)
        elif choice == 1:  # Hint
            self._show_hint(selected_challenge)
        # Otherwise return to main menu

    def _attempt_challenge(self, challenge: Challenge):
        """
        Allow the player to attempt a challenge.

        Args:
            challenge: The challenge to attempt
        """
        attempt_again = True
        
        while attempt_again:
            self.ui.clear_screen()
            self.ui.print_subtitle(f"Challenge: {challenge.name}")

            # Show simplified description again
            self.ui.print_info(challenge.description)

            # Get user's solution
            user_code = self.ui.code_editor()

            if not user_code.strip():
                self.ui.print_warning(
                    "No solution provided. Returning to main menu.")
                input("\nPress Enter to continue...")
                return

            # Show "evaluating" animation
            self.ui.print_info("Evaluating your solution...")

            try:
                # Create namespace for executing code
                namespace = {}
                
                # Execute user code
                exec(user_code, namespace)
                
                # Get the function name from challenge ID
                function_name = challenge.id.replace("-", "_")
                
                # Try to find the function in namespace
                if function_name not in namespace:
                    # Look for any callable that isn't a built-in
                    for name, obj in namespace.items():
                        if callable(obj) and not name.startswith("__"):
                            function_name = name
                            break
                
                if function_name in namespace and callable(namespace[function_name]):
                    # Get user solution function
                    user_solution = namespace[function_name]
                    
                    # Evaluate solution
                    result = challenge.attempt_solution(user_solution)
                    
                    # Display results
                    self.ui.clear_screen()
                    self.ui.print_subtitle("Challenge Results")

                    if result["success"]:
                        self.ui.print_success(
                            "Congratulations! Your solution passed all test cases.")
                        
                        try:
                            # Award XP
                            leveled_up = self.character.add_experience(challenge.xp_reward)
                            
                            # Mark challenge as completed
                            self.character.complete_challenge(
                                challenge_name=challenge.name,
                                skill=challenge.primary_skill if hasattr(challenge, 'primary_skill') else None,
                                xp_gained=challenge.xp_reward
                            )
                            
                            self.ui.print_success(f"You earned {challenge.xp_reward} XP!")
                            
                            # Show level up message if applicable
                            if leveled_up:
                                self.ui.print_success(
                                    f"Level up! You are now level {self.character.level}!")
                                
                                # Check if new areas were unlocked
                                if hasattr(self.character, 'unlocked_areas') and len(self.character.unlocked_areas) > 1:
                                    new_area = self.character.unlocked_areas[-1]
                                    self.ui.print_success(
                                        f"You've unlocked a new area: {new_area}!")
                        except Exception as e:
                            self.ui.print_error(f"Error updating character progress: {str(e)}")
                            
                        # Challenge completed successfully, no need to retry
                        attempt_again = False
                    else:
                        self.ui.print_warning(
                            "Your solution did not pass all test cases.")
                    
                    # Show feedback
                    if "feedback" in result and result["feedback"]:
                        self.ui.print_subtitle("Feedback:")
                        for feedback in result["feedback"]:
                            self.ui.print_info(feedback)
                    
                    # Show test case results if available
                    if "test_cases" in result and result["test_cases"]:
                        self.ui.print_subtitle("Test Cases:")
                        for i, tc in enumerate(result["test_cases"]):
                            if tc.get("passed", False):
                                self.ui.print_success(f"Test {i+1}: Passed")
                            else:
                                self.ui.print_error(f"Test {i+1}: Failed")
                                if "error" in tc:
                                    self.ui.print_error(f"  Error: {tc['error']}")
                    
                    # Ask if the user wants to try again if the solution failed
                    if not result["success"]:
                        retry_choice = self.ui.menu("Would you like to try again?", ["Yes", "No"])
                        attempt_again = (retry_choice == 0)  # Yes is index 0
                    
                else:
                    self.ui.print_error(f"Could not find a solution function in your code. The function should be named '{function_name}'.")
                    retry_choice = self.ui.menu("Would you like to try again?", ["Yes", "No"])
                    attempt_again = (retry_choice == 0)  # Yes is index 0
                    
            except Exception as e:
                self.ui.print_error(f"Error evaluating your solution: {str(e)}")
                retry_choice = self.ui.menu("Would you like to try again?", ["Yes", "No"])
                attempt_again = (retry_choice == 0)  # Yes is index 0
            
            if attempt_again:
                continue
            else:
                input("\nPress Enter to continue...")
                return

    def _show_hint(self, challenge: Challenge):
        """
        Show a hint for a challenge.

        Args:
            challenge: The challenge to get a hint for
        """
        self.ui.clear_screen()
        self.ui.print_subtitle(f"Hint for: {challenge.name}")

        if challenge.hints:
            hint = random.choice(challenge.hints)
            self.ui.print_info(hint)
        else:
            self.ui.print_warning("No hints available for this challenge.")

        input("\nPress Enter to continue...")

    def _view_character(self):
        """Display detailed character information."""
        self.ui.clear_screen()
        self.ui.print_subtitle(f"Character: {self.character.name}")

        stats = self.character.get_stats()

        # Display basic stats
        self.ui.print_info(f"Class: {stats['class']}")
        self.ui.print_info(f"Level: {stats['level']}")
        self.ui.print_info(
            f"Experience: {stats['experience']}/{stats['xp_to_next_level']} to next level")
        self.ui.print_info(
            f"Challenges Completed: {stats['challenges_completed']}")

        # Display skills
        self.ui.print_subtitle("Skills:")
        for skill_name, level in stats['skills'].items():
            self.ui.print_info(f"{skill_name}: Level {level}")

        # Display unlocked areas
        self.ui.print_subtitle("Unlocked Areas:")
        for area in stats['unlocked_areas']:
            self.ui.print_success(f"✓ {area}")

        input("\nPress Enter to continue...")

    def _show_tutorial(self):
        """Show the tutorial for the game."""
        # In a real implementation, this would use the Tutorial class
        # For now, just display some basic instructions

        self.ui.clear_screen()
        self.ui.print_title("Tutorial")

        tutorial_text = """
        Welcome to Fantasy Coding Quest!
        
        This game combines coding practice with RPG elements.
        
        HOW TO PLAY:
        1. Create a character or load a saved game
        2. Select challenges from your unlocked areas
        3. Write Python code to solve the challenges
        4. Earn XP and level up your character
        5. Unlock new areas as you progress
        
        TAKING ON CHALLENGES:
        - Read the challenge description carefully
        - Write your solution in the code editor
        - Type 'END' on a new line when you're finished
        - The game will evaluate your solution and give you feedback
        
        CHARACTER PROGRESSION:
        - As you complete challenges, you'll earn XP
        - When you have enough XP, you'll level up
        - Leveling up unlocks new areas with harder challenges
        - Your skills will also improve as you complete related challenges
        
        Good luck on your coding adventure!
        """

        self.ui.print_info(tutorial_text)
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    game = Game()
    game.start()
