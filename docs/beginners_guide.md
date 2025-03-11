# Complete Beginner's Guide to Fantasy Coding Quest

This guide walks you through starting and playing Fantasy Coding Quest step-by-step, assuming you have no prior coding or technical experience.

## First Time Setup

### Installing Fantasy Coding Quest (Windows)

1. **Install Python**:

   - Visit [python.org](https://www.python.org/downloads/)
   - Click the big yellow "Download Python" button
   - Run the downloaded file
   - CHECK the box that says "Add Python to PATH" (very important!)
   - Click "Install Now"
   - Wait for installation to complete, then click "Close"

2. **Get Fantasy Coding Quest**:

   - Download the Fantasy Coding Quest ZIP file
   - Right-click the ZIP file and select "Extract All..."
   - Choose a location you can find easily (like your Desktop)
   - Click "Extract"

3. **Open Command Prompt**:

   - Press Windows key + R
   - Type `cmd` and press Enter
   - A black window will appear - this is the Command Prompt

4. **Navigate to the Game Folder**:

   - Type `cd ` (with a space after "cd")
   - Drag and drop the Fantasy Coding Quest folder onto the Command Prompt window
   - Press Enter

5. **Install Required Packages**:
   - Type this command exactly as written:
     ```
     pip install -r requirements.txt
     ```
   - Press Enter and wait for installation to complete

### Installing Fantasy Coding Quest (Mac)

1. **Install Python**:

   - Visit [python.org](https://www.python.org/downloads/)
   - Click the big yellow "Download Python" button
   - Run the downloaded file and follow installation instructions
   - Complete the installation

2. **Get Fantasy Coding Quest**:

   - Download the Fantasy Coding Quest ZIP file
   - Double-click the ZIP file to extract it
   - Move the extracted folder to a location you can find easily

3. **Open Terminal**:

   - Press Command + Space to open Spotlight Search
   - Type "Terminal" and press Enter
   - A window with a command line will appear

4. **Navigate to the Game Folder**:

   - Type `cd ` (with a space after "cd")
   - Drag and drop the Fantasy Coding Quest folder onto the Terminal window
   - Press Enter

5. **Install Required Packages**:
   - Type this command exactly as written:
     ```
     pip3 install -r requirements.txt
     ```
   - Press Enter and wait for installation to complete

## Starting the Game

1. **Open Command Prompt/Terminal** as you did during installation
2. **Navigate to the Game Folder** as you did during installation
3. **Start the Game**:
   - On Windows, type:
     ```
     python -m src.main
     ```
   - On Mac, type:
     ```
     python3 -m src.main
     ```
   - Press Enter
4. The game should start and display the Fantasy Coding Quest title screen!

## Creating Your Character

1. Select "New Game" by typing `1` and pressing Enter
2. Enter your character's name when prompted
3. Choose a character class:
   - Algorithm Wizard: Good for logic puzzles
   - Data Structure Paladin: Good for organizing information
   - Debugging Rogue: Good at finding mistakes
   - System Design Druid: Good at big-picture thinking
   - Fullstack Bard: Jack of all trades
4. Type the number that corresponds to your choice and press Enter

## Game Navigation

- The game uses number-based menus
- Type the number next to your desired option and press Enter
- You'll see options like:
  - View Map
  - Take on a Challenge
  - View Character
  - Save Game
  - Exit Game

## Taking Your First Challenge

1. From the main menu, select "Take on a Challenge"
2. Choose an area to explore (beginners should start with "Algorithm Forest")
3. Select a challenge from the list
4. Read the challenge description carefully
5. Choose "Attempt Challenge" to begin coding

## Using the Code Editor

When you attempt a challenge, you'll enter the code editor:

1. You'll see a template function with comments
2. Type your code directly in the terminal
3. Use proper indentation (spaces at the beginning of lines) for Python code
4. When you're finished, type `END` on a new line
5. The game will evaluate your solution and tell you if it worked

## Tips for First-Time Coders

- **Read the full description** before attempting a solution
- **Use hints** when you get stuck
- **Learn from failures** by reading error messages carefully
- **Be patient** - learning to code takes time
- **Use online resources** to learn coding basics if needed

## Basic Python Concepts You'll Need

- **Variables**: Store values (e.g., `x = 5`)
- **Loops**: Repeat actions (e.g., `for i in range(5):`)
- **Conditions**: Make decisions (e.g., `if x > 10:`)
- **Functions**: Groups of reusable code (e.g., `def add(a, b):`)
- **Return statements**: Send values back (e.g., `return result`)

## Example: Solving Your First Challenge

Here's how to solve the "Two Sum" challenge:

1. Read the problem carefully - you need to find two numbers in a list that add up to a target value
2. The function should look like this:
   ```python
   def two_sum(nums, target):
       # Your code here
       pass
   ```
3. A simple solution would be:
   ```python
   def two_sum(nums, target):
       for i in range(len(nums)):
           for j in range(i + 1, len(nums)):
               if nums[i] + nums[j] == target:
                   return [i, j]
       return []
   ```
4. Type this code in the editor, then type `END` on a new line
5. The game will tell you if your solution is correct!

## Saving Your Progress

- From the main menu, select "Save Game"
- Your progress will be saved and can be loaded later
- When starting the game, choose "Load Game" to continue where you left off

## Getting Help

If you get stuck:

1. Use the "Get a Hint" option when viewing a challenge
2. Look up basic Python tutorials online
3. Practice simpler challenges before attempting harder ones
4. Remember that learning to code is a journey - don't get discouraged!

Enjoy your adventure in Fantasy Coding Quest!
