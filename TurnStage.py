from enum import Enum, auto

class TurnStage(Enum):
    """Stages of a players turn"""
    ROLL1 = auto()
    ROLL2 = auto()
    ROLL3 = auto()
    SILVERTRAY = auto()
    ROUND4 = auto()
    BONUS = auto()
    POSTROUND = auto()