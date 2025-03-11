# Fantasy Coding Quest: Absolute Beginner's Guide

This guide assumes you have **no prior experience** with programming or using command-line tools. We'll walk through every step in detail.

## What is Fantasy Coding Quest?

Fantasy Coding Quest is a game that teaches you coding through fun, fantasy-themed challenges. You'll play as a character in a magical world, solving puzzles that teach you real programming skills.

## Step 1: Installing Python

Before you can play the game, you need to install Python (the programming language).

### On Windows:

1. **Open your web browser** (like Chrome, Firefox, or Edge)
2. **Visit** [python.org/downloads](https://www.python.org/downloads/)
3. **Click** the big yellow button that says "Download Python" (it will show a version number like 3.9.7)
4. **Save** the file when prompted
5. **Find the downloaded file** in your Downloads folder
6. **Double-click** the file to run it
7. **IMPORTANT**: Check the box that says "Add Python to PATH" ✅
8. **Click** "Install Now"
9. **Wait** for the installation to complete
10. **Click** "Close" when it's done

### On Mac:

1. **Open your web browser**
2. **Visit** [python.org/downloads](https://www.python.org/downloads/)
3. **Click** the big yellow button that says "Download Python"
4. **Save** the file when prompted
5. **Find the downloaded file** in your Downloads folder
6. **Double-click** the file to run it
7. **Follow** the installation instructions
8. **Click** "Close" when it's done

## Step 2: Downloading Fantasy Coding Quest

1. **Download** the Fantasy Coding Quest ZIP file from [github.com/wrek34/fantasy-coding-quest/archive/refs/heads/main.zip](https://github.com/wrek34/fantasy-coding-quest/archive/refs/heads/main.zip)
2. **Find the downloaded ZIP file** in your Downloads folder

### On Windows:

3. **Right-click** the ZIP file
4. **Select** "Extract All..."
5. **Choose** a location you can find easily (like your Desktop)
6. **Click** "Extract"

### On Mac:

3. **Double-click** the ZIP file to extract it
4. **Move** the extracted folder to a location you can find easily (like your Desktop)

## Step 3: Opening the Command Line

The command line is a text-based way to interact with your computer. It might look intimidating at first, but you'll only need a few simple commands.

### On Windows:

1. **Press** the Windows key + R
2. **Type** `cmd` and press Enter
3. A black window will appear - this is the Command Prompt

### On Mac:

1. **Press** Command + Space to open Spotlight Search
2. **Type** "Terminal" and press Enter
3. A window will appear - this is the Terminal

## Step 4: Navigating to the Game Folder

Now you need to tell the command line where to find the game files.

### On Windows:

1. **Type** `cd ` (with a space after "cd")
2. **Drag and drop** the Fantasy Coding Quest folder onto the Command Prompt window
   - This will automatically fill in the path to the folder
3. **Press** Enter

### On Mac:

1. **Type** `cd ` (with a space after "cd")
2. **Drag and drop** the Fantasy Coding Quest folder onto the Terminal window
   - This will automatically fill in the path to the folder
3. **Press** Enter

## Step 5: Installing Game Requirements

The game needs some additional Python libraries to run. Let's install them:

### On Windows:

1. **Type** this command exactly as written:
   ```
   pip install -r requirements.txt
   ```
2. **Press** Enter
3. **Wait** for installation to complete (you'll see text scrolling)

### On Mac:

1. **Type** this command exactly as written:
   ```
   pip3 install -r requirements.txt
   ```
2. **Press** Enter
3. **Wait** for installation to complete (you'll see text scrolling)

## Step 6: Starting the Game

Now you're ready to start the game!

### On Windows:

1. **Type** this command:
   ```
   python -m src.main
   ```
2. **Press** Enter

### On Mac:

1. **Type** this command:
   ```
   python3 -m src.main
   ```
2. **Press** Enter

## Step 7: Playing the Game

The game should now be running! Here's how to play:

1. **Select "Tutorial"** from the main menu by typing the corresponding number and pressing Enter
2. **Follow** the tutorial instructions to learn the basics
3. **Create a character** when prompted
4. **Start with the easiest challenges** in the Algorithm Forest
5. **Read challenge descriptions carefully**
6. **Use hints** if you get stuck
7. **Don't be afraid to try again** if your solution doesn't work

## Troubleshooting Common Issues

### "Python is not recognized as an internal or external command"

This means Python wasn't added to your PATH during installation.

1. **Reinstall Python**
2. **Make sure to check** "Add Python to PATH" during installation

### "No module named src"

You might not be in the correct folder.

1. **Make sure** you're in the Fantasy Coding Quest folder
2. You should see files like "requirements.txt" when you type `dir` (Windows) or `ls` (Mac)

### Game crashes or shows errors

1. **Take a screenshot** of the error
2. **Try reinstalling** the game requirements:
   ```
   pip install -r requirements.txt
   ```
   (or `pip3` on Mac)

## Your First Coding Challenge

When you start the game, look for "The Greeting Spell" challenge:

1. This challenge asks you to create a function that returns "Hello, magical world!"
2. The solution is:
   ```python
   def hello_world():
       return "Hello, magical world!"
   ```
3. Type this code exactly, then type `END` on a new line
4. The game will check your solution and give you feedback

Congratulations, you're now a coding adventurer! Continue with more challenges to improve your skills.
