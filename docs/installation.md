# Installation Guide for Fantasy Coding Quest

This guide will walk you through the process of installing Fantasy Coding Quest on your computer.

## System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux
- **Python**: Version 3.8 or higher
- **Disk Space**: At least 100MB of free space
- **RAM**: 2GB minimum (4GB recommended)

## Step-by-Step Installation

### 1. Install Python

If you don't have Python installed, download and install it first:

- **Windows**: Download from [python.org](https://www.python.org/downloads/) and run the installer
  - ✅ Make sure to check "Add Python to PATH" during installation
- **macOS**:
  - Option 1: Download from [python.org](https://www.python.org/downloads/)
  - Option 2: Use Homebrew: `brew install python`
- **Linux**:
  - Ubuntu/Debian: `sudo apt-get install python3 python3-pip`
  - Fedora: `sudo dnf install python3 python3-pip`

### 2. Download Fantasy Coding Quest

#### Using Git (Recommended)

If you have Git installed:

```bash
git clone https://github.com/wrek34/fantasy-coding-quest.git
cd fantasy-coding-quest
```

#### Without Git

1. Go to https://github.com/wrek34/fantasy-coding-quest
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract the ZIP file to a folder of your choice
5. Open a terminal/command prompt and navigate to the extracted folder

### 3. Set Up a Virtual Environment

Creating a virtual environment is recommended to avoid conflicts with other Python packages:

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

You'll know the virtual environment is active when you see `(venv)` at the beginning of your command line.

### 4. Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 5. Run the Game

```bash
python -m src.main
```

## Troubleshooting

### "Python is not recognized as an internal or external command"

This means Python wasn't added to your PATH during installation. Options:

1. Reinstall Python and check "Add Python to PATH"
2. Add Python to your PATH manually (search online for instructions for your OS)

### "No module named src"

Make sure you're running the command from the main fantasy-coding-quest directory.

### "No module named [package name]"

Try reinstalling the dependencies:

```bash
pip install -r requirements.txt
```

### Game Crashes on Startup

Check that you have the correct Python version (3.8+):

```bash
python --version
```

## Uninstalling

To uninstall Fantasy Coding Quest:

1. Delete the game directory
2. Delete the virtual environment if you created one
