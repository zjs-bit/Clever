from dataclasses import dataclass
from Color import Color
from enum import Enum,auto

@dataclass
class DiceAction:
    color: Color
    area: Color = None
    value: int = None
    placement: tuple = None

    def __post_init__(self):
        if self.color is not Color.WHITE:
            self.area = self.color
        
class StrategicAction(Enum):
    #Only 1 in this version of clever
    REROLL = auto()
    PASS = auto()