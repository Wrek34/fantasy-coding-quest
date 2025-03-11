import os
import sys
import time
from typing import List, Dict, Any, Optional
import pyfiglet
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class UI:
    """Terminal user interface for Fantasy Coding Quest."""
    
    def __init__(self):
        """Initialize UI with default values."""
        self.clear_screen()
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_title(text: str):
        """Print a title using ASCII art."""
        title_art = pyfiglet.figlet_format(text, font="big")
        print(Fore.CYAN + title_art)
    
    @staticmethod
    def print_subtitle(text: str):
        """Print a subtitle."""
        print(Fore.YELLOW + Style.BRIGHT + "\n" + "=" * 60)
        print(Fore.YELLOW + Style.BRIGHT + text.center(60))
        print(Fore.YELLOW + Style.BRIGHT + "=" * 60 + "\n")
    
    @staticmethod
    def print_section(text: str):
        """Print a section header."""
        print(Fore.GREEN + Style.BRIGHT + "\n" + text)
        print(Fore.GREEN + Style.BRIGHT + "-" * len(text) + "\n")
    
    @staticmethod
    def print_success(text: str):
        """Print a success message."""
        print(Fore.GREEN + "✓ " + text)
    
    @staticmethod
    def print_error(text: str):
        """Print an error message."""
        print(Fore.RED + "✗ " + text)
    
    @staticmethod
    def print_info(text: str):
        """Print an info message."""
        print(Fore.CYAN + "ℹ " + text)
    
    @staticmethod
    def print_warning(text: str):
        """Print a warning message."""
        print(Fore.YELLOW + "⚠ " + text)
    
    def prompt(self, message: str, default: str = "") -> str:
        """Prompt the user for input."""
        if default:
            response = input(f"{Fore.MAGENTA}{message} [{default}]: {Style.RESET_ALL}")
            return response if response else default
        return input(f"{Fore.MAGENTA}{message}: {Style.RESET_ALL}")
    
    def menu(self, title: str, options: List[str]) -> int:
        """
        Display a menu and get the user's choice.
        
        Args:
            title: The title of the menu
            options: List of menu options
            
        Returns:
            The index of the selected option (0-based)
        """
        self.print_section(title)
        
        for i, option in enumerate(options, 1):
            print(f"{Fore.CYAN}{i}. {Style.RESET_ALL}{option}")
        
        while True:
            try:
                choice = int(self.prompt("\nEnter your choice"))
                if 1 <= choice <= len(options):
                    return choice - 1
                self.print_error(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                self.print_error("Please enter a valid number")
    
    def display_character_stats(self, stats: Dict[str, Any]):
        """Display character statistics."""
        self.print_section(f"Character: {stats['name']} - Level {stats['level']} {stats['class']}")
        print(f"XP: {stats['experience']}/{stats['xp_to_next_level']}")
        print(f"Challenges Completed: {stats['challenges_completed']}")
        
        self.print_section("Skills")
        for skill, level in stats['skills'].items():
            skill_bar = "█" * int(level * 2)
            print(f"{skill.ljust(25)}: {skill_bar} ({level:.1f}/10)")
        
        self.print_section("Inventory")
        if stats['inventory']:
            for item in stats['inventory']:
                print(f"- {item}")
        else:
            print("Empty")
        
        self.print_section("Unlocked Areas")
        for area in stats['unlocked_areas']:
            print(f"- {area}")
    
    def display_challenge(self, challenge: Dict[str, Any]):
        """Display a challenge."""
        self.print_subtitle(f"{challenge['name']}")
        print(f"{Fore.CYAN}Area: {Style.RESET_ALL}{challenge['area']}")
        print(f"{Fore.CYAN}Difficulty: {Style.RESET_ALL}{challenge['difficulty']}")
        print(f"{Fore.CYAN}Type: {Style.RESET_ALL}{challenge['challenge_type']}")
        print(f"{Fore.CYAN}XP Reward: {Style.RESET_ALL}{challenge['xp_reward']}")
        if challenge['time_limit_seconds']:
            print(f"{Fore.CYAN}Time Limit: {Style.RESET_ALL}{challenge['time_limit_seconds']} seconds")
        
        self.print_section("Description")
        print(challenge['description'])
    
    def display_challenge_results(self, results: Dict[str, Any]):
        """Display the results of a challenge attempt."""
        if results['success']:
            self.print_success("Challenge Completed Successfully!")
            print(f"Time taken: {results['time_taken']:.2f} seconds")
            
            if 'test_cases' in results:
                self.print_section("Test Cases")
                for i, case in enumerate(results['test_cases'], 1):
                    status = Fore.GREEN + "✓ Passed" if case['passed'] else Fore.RED + "✗ Failed"
                    print(f"Test {i}: {status}")
                    if not case['passed'] and 'error' in case:
                        print(f"  Error: {case['error']}")
        else:
            self.print_error("Challenge Failed")
            if 'error' in results:
                print(f"Error: {results['error']}")
            
            if 'test_cases' in results:
                self.print_section("Test Cases")
                for i, case in enumerate(results['test_cases'], 1):
                    status = Fore.GREEN + "✓ Passed" if case['passed'] else Fore.RED + "✗ Failed"
                    print(f"Test {i}: {status}")
                    if not case['passed'] and 'error' in case:
                        print(f"  Error: {case['error']}")
    
    def code_editor(self, initial_code: str = "") -> str:
        """
        Simple in-terminal code editor.
        For now, just a placeholder that prompts for code input.
        In a real implementation, might integrate with an external editor.
        """
        self.print_section("Code Editor")
        print("Enter your solution below. Type 'END' on a new line when finished.")
        print(Fore.CYAN + initial_code)
        
        lines = []
        line = input()
        while line != "END":
            lines.append(line)
            line = input()
        
        return initial_code + "\n".join(lines)
    
    def loading_animation(self, message: str, duration: float = 1.0):
        """Display a simple loading animation."""
        frames = ["|", "/", "-", "\\"]
        end_time = time.time() + duration
        
        i = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r{message} {frames[i % len(frames)]}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        
        sys.stdout.write(f"\r{message} Done!{' ' * 10}\n")