from enum import Enum

class Level(Enum):
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]