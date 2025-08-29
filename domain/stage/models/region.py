from enum import Enum

class Region(Enum):
    KO_KR = "ko_kr"
    EN_US = "en_us"
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]