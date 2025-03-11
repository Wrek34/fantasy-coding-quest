class Tutorial:
    """Provides an interactive tutorial for first-time players."""

    def __init__(self, ui):
        """Initialize the tutorial with a UI instance."""
        self.ui = ui
        self.steps = [
            {
                "title": "Welcome to Fantasy Coding Quest!",
                "content": """
                This tutorial will guide you through the basics of playing the game.
                
                Fantasy Coding Quest combines coding practice with RPG elements.
                As you solve coding challenges, your character will level up and unlock new areas!
                
                Press Enter to continue...
                """
            },
            {
                "title": "Understanding the Interface",
                "content": """
                The game uses a text-based interface. You'll see:
                
                - Menus: Select options by typing the corresponding number
                - Character stats: Shows your level, XP, and skills
                - Challenge descriptions: Details about each coding problem
                - Code editor: Where you'll write your solutions
                
                Press Enter to continue...
                """
            },
            {
                "title": "Your Character",
                "content": """
                Your character has:
                
                - A class that determines starting skill bonuses
                - Skills that improve as you complete related challenges
                - XP that helps you level up
                - Unlocked areas where you can find challenges
                
                Press Enter to continue...
                """
            },
            {
                "title": "Taking on Challenges",
                "content": """
                Challenges are coding problems presented as fantasy quests:
                
                1. Select a challenge from your current area
                2. Read the description carefully
                3. Choose to attempt the challenge or get a hint
                4. Write your solution in the code editor
                5. Type "END" on a new line when you're done
                6. The game will evaluate your solution
                
                Press Enter to continue...
                """
            },
            {
                "title": "Writing Solutions",
                "content": """
                When writing a solution:
                
                - Use proper Python syntax
                - Make sure your function has the correct name and parameters
                - Return the expected value type
                - Use indentation (spaces) correctly
                
                Don't worry if you're new to coding - you can use hints and try as many times as needed.
                
                Press Enter to continue...
                """
            },
            {
                "title": "Progression",
                "content": """
                As you complete challenges:
                
                - You'll earn XP to level up
                - Your skills will improve
                - You'll unlock new areas with harder challenges
                - You can save your progress at any time
                
                Press Enter to continue...
                """
            },
            {
                "title": "Tutorial Complete!",
                "content": """
                You're now ready to begin your adventure in Fantasy Coding Quest!
                
                Remember, the goal is to learn and improve your coding skills while having fun.
                
                Good luck, adventurer!
                
                Press Enter to start your journey...
                """
            }
        ]

    def run(self):
        """Run the tutorial sequence."""
        self.ui.clear_screen()

        for step in self.steps:
            self.ui.clear_screen()
            self.ui.print_subtitle(step["title"])
            self.ui.print_info(step["content"])
            input()  # Wait for Enter key
