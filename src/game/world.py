from typing import Dict, List, Optional, Any
from enum import Enum


class Area(Enum):
    ALGORITHM_FOREST = "Algorithm Forest"
    DATA_STRUCTURE_MOUNTAINS = "Data Structure Mountains"
    DATABASE_DUNGEON = "Database Dungeon"
    SYSTEM_DESIGN_CITADEL = "System Design Citadel"
    WEB_DEVELOPMENT_SHORES = "Web Development Shores"
    CLOUD_KINGDOM = "Cloud Kingdom"


class World:
    """Represents the fantasy world map and state."""
    
    def __init__(self):
        """Initialize the world with default areas and connections."""
        self.areas = {
            Area.ALGORITHM_FOREST: {
                "description": "A mystical forest where algorithmic challenges lurk behind every tree. "
                               "The perfect starting point for new adventurers.",
                "connected_areas": [Area.DATA_STRUCTURE_MOUNTAINS],
                "difficulty": 1,
                "challenge_types": ["sorting", "searching", "recursion"],
                "unlocked": True
            },
            Area.DATA_STRUCTURE_MOUNTAINS: {
                "description": "Towering peaks where each cliff and valley represents a different data structure. "
                               "A challenging area for those who have mastered the basics.",
                "connected_areas": [Area.ALGORITHM_FOREST, Area.DATABASE_DUNGEON, Area.SYSTEM_DESIGN_CITADEL],
                "difficulty": 2,
                "challenge_types": ["arrays", "linked_lists", "trees", "graphs"],
                "unlocked": False
            },
            Area.DATABASE_DUNGEON: {
                "description": "A sprawling underground network of caverns filled with database challenges. "
                               "The echoes of SQL queries bounce off the walls.",
                "connected_areas": [Area.DATA_STRUCTURE_MOUNTAINS, Area.SYSTEM_DESIGN_CITADEL],
                "difficulty": 3,
                "challenge_types": ["sql", "nosql", "data_modeling"],
                "unlocked": False
            },
            Area.SYSTEM_DESIGN_CITADEL: {
                "description": "A grand fortress where architects come to test their system design knowledge. "
                               "Each room presents a different scalability challenge.",
                "connected_areas": [Area.DATA_STRUCTURE_MOUNTAINS, Area.DATABASE_DUNGEON, Area.WEB_DEVELOPMENT_SHORES],
                "difficulty": 4,
                "challenge_types": ["architecture", "scalability", "reliability"],
                "unlocked": False
            },
            Area.WEB_DEVELOPMENT_SHORES: {
                "description": "A beautiful coastline where the waves of frontend and backend development crash together. "
                               "Build web applications to proceed further.",
                "connected_areas": [Area.SYSTEM_DESIGN_CITADEL, Area.CLOUD_KINGDOM],
                "difficulty": 3,
                "challenge_types": ["frontend", "backend", "api_design"],
                "unlocked": False
            },
            Area.CLOUD_KINGDOM: {
                "description": "A kingdom floating among the clouds, representing the pinnacle of cloud computing challenges. "
                               "Only the most skilled adventurers can reach this realm.",
                "connected_areas": [Area.WEB_DEVELOPMENT_SHORES],
                "difficulty": 5,
                "challenge_types": ["cloud_services", "serverless", "devops"],
                "unlocked": False
            }
        }
        
        # Map visualization (ASCII for now)
        self.map_ascii = """
                    ☁️ CLOUD KINGDOM ☁️
                         /   
                        /    
             🏖️ WEB DEV SHORES 🏖️  
                    /        
                   /         
          🏰 SYSTEM DESIGN CITADEL 🏰
               /        \\   
              /          \\  
        🔍 DATABASE      🏔️ DATA STRUCTURE
        🔍 DUNGEON       🏔️ MOUNTAINS
                           \\  
                            \\ 
                      🌲 ALGORITHM FOREST 🌲
        """
    
    def unlock_area(self, area: Area) -> None:
        """Unlock an area."""
        if area in self.areas:
            self.areas[area]["unlocked"] = True
    
    def get_unlocked_areas(self) -> List[Area]:
        """Return a list of all unlocked areas."""
        return [area for area in self.areas if self.areas[area]["unlocked"]]
    
    def get_area_details(self, area: Area) -> Dict[str, Any]:
        """Return details about a specific area."""
        if area in self.areas:
            return self.areas[area]
        return None
    
    def get_connected_areas(self, area: Area) -> List[Area]:
        """Return a list of areas connected to the given area."""
        if area in self.areas:
            return [connected_area for connected_area in self.areas[area]["connected_areas"] 
                   if self.areas[connected_area]["unlocked"]]
        return []
    
    def display_map(self) -> str:
        """Return a string representation of the world map."""
        # For now, return the ASCII map
        # In a future version, we could highlight unlocked areas
        return self.map_ascii