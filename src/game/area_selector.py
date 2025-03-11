from typing import List, Optional
from src.game.world import World, Area


class AreaSelector:
    """Handles area selection and unlocking mechanics."""

    def __init__(self, world: World):
        """Initialize the area selector with a world instance."""
        self.world = world

    def get_available_areas(self, unlocked_areas: List[str]) -> List[Area]:
        """
        Get a list of all available areas that the player has unlocked.

        Args:
            unlocked_areas: List of area names the player has unlocked

        Returns:
            List of corresponding Area enum values
        """
        available = []

        for area in Area:
            if area.value in unlocked_areas:
                available.append(area)

        return available

    def select_area(self, ui, unlocked_areas: List[str]) -> Optional[Area]:
        """
        Prompt the player to select an area using the UI.

        Args:
            ui: UI instance for displaying prompts
            unlocked_areas: List of area names the player has unlocked

        Returns:
            Selected Area enum value, or None if cancelled
        """
        available_areas = self.get_available_areas(unlocked_areas)

        if not available_areas:
            ui.print_warning("You haven't unlocked any areas yet.")
            return None

        # Create a list of area names and descriptions
        area_options = []
        for area in available_areas:
            details = self.world.get_area_details(area)
            area_options.append(
                f"{area.value} - {details['difficulty']} Difficulty")

        area_options.append("Return to Main Menu")

        # Let the player choose an area
        ui.clear_screen()
        ui.print_subtitle("Select an Area to Explore")

        choice = ui.menu("Choose an area:", area_options)

        # Return the selected area, or None if the player chose to return
        if choice < len(available_areas):
            return available_areas[choice]

        return None

    def get_area_challenges(self, area: Area, all_challenges: dict) -> List[dict]:
        """
        Get all challenges for a specific area.

        Args:
            area: The area to get challenges for
            all_challenges: Dictionary of all available challenges

        Returns:
            List of challenges in the specified area
        """
        area_challenges = []

        for challenge_id, challenge in all_challenges.items():
            if challenge.area == area.value:
                area_challenges.append({
                    "id": challenge_id,
                    "name": challenge.name,
                    "difficulty": challenge.difficulty.value,
                    "type": challenge.challenge_type.value,
                    "xp_reward": challenge.xp_reward
                })

        return area_challenges
