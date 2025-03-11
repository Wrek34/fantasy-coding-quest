import os
import sys

def check_directory_structure():
    """Check if the project directory structure is correct."""
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
    
    required_files = [
        "src/__init__.py",
        "src/game/__init__.py",
        "src/challenges/__init__.py",
        "src/challenges/challenges/__init__.py",
        "src/challenges/challenges/algorithms/__init__.py",
        "src/challenges/challenges/data_structures/__init__.py",
        "src/ai/__init__.py",
        "src/main.py",
        "src/game/character.py",
        "src/game/world.py",
        "src/game/ui.py",
        "src/game/save_manager.py",
        "src/challenges/challenge_base.py",
    ]
    
    # Check directories
    missing_dirs = []
    for directory in required_dirs:
        if not os.path.isdir(directory):
            missing_dirs.append(directory)
    
    # Check files
    missing_files = []
    for file in required_files:
        if not os.path.isfile(file):
            missing_files.append(file)
    
    if missing_dirs:
        print("Missing directories:")
        for directory in missing_dirs:
            print(f"  - {directory}")
        print("\nPlease create these directories.")
    
    if missing_files:
        print("Missing files:")
        for file in missing_files:
            print(f"  - {file}")
        print("\nPlease create these files.")
    
    if not missing_dirs and not missing_files:
        print("Directory structure looks good!")
        return True
    
    return False

if __name__ == "__main__":
    print("Checking Fantasy Coding Quest project structure...")
    if check_directory_structure():
        print("\nYou can now run the game with: python -m src.main")
    else:
        print("\nPlease fix the directory structure before running the game.") 