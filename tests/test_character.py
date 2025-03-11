import pytest
from src.game.character import Character, CharacterClass, Skill


def test_character_creation():
    """Test that a character can be created with the expected attributes."""
    character = Character(
        name="Test Character",
        character_class=CharacterClass.ALGORITHM_WIZARD
    )

    assert character.name == "Test Character"
    assert character.character_class == CharacterClass.ALGORITHM_WIZARD
    assert character.level == 1
    assert character.experience == 0
    assert character.challenges_completed == 0
    assert len(character.inventory) == 0
    assert "Algorithm Forest" in character.unlocked_areas


def test_character_leveling():
    """Test that a character levels up correctly when gaining XP."""
    character = Character(
        name="Test Character",
        character_class=CharacterClass.ALGORITHM_WIZARD
    )

    # Character starts at level 1 with 0 XP
    assert character.level == 1
    assert character.experience == 0

    # Add 50 XP (not enough to level up)
    character.add_experience(50)
    assert character.level == 1
    assert character.experience == 50

    # Add 50 more XP (should level up to level 2)
    character.add_experience(50)
    assert character.level == 2
    assert character.experience == 0  # XP resets after leveling

    # Add 150 XP (should level up to level 3)
    character.add_experience(150)
    assert character.level == 3
    assert character.experience == 0


def test_character_skill_improvement():
    """Test that skills improve when completing challenges."""
    character = Character(
        name="Test Character",
        character_class=CharacterClass.ALGORITHM_WIZARD
    )

    # Get initial Arrays skill value
    initial_skill = character.skills[Skill.ARRAYS]

    # Complete a challenge related to Arrays
    character.complete_challenge(
        challenge_name="Test Challenge",
        skill=Skill.ARRAYS,
        xp_gained=50
    )

    # Skill should improve
    assert character.skills[Skill.ARRAYS] > initial_skill

    # Challenge should be counted
    assert character.challenges_completed == 1


def test_area_unlocking():
    """Test that new areas are unlocked at specific levels."""
    character = Character(
        name="Test Character",
        character_class=CharacterClass.ALGORITHM_WIZARD
    )

    # Start with only Algorithm Forest
    assert len(character.unlocked_areas) == 1
    assert "Algorithm Forest" in character.unlocked_areas

    # Level up to 5 (should unlock a new area)
    for _ in range(4):  # 4 more levels to reach level 5
        character.add_experience(100)  # Enough to level up once

    assert character.level == 5
    assert len(character.unlocked_areas) == 2
