from dataclasses import dataclass
from enum import Enum, auto
from Color import Color

class BonusType(Enum):
    """"Bonus Types"""
    NONE = auto()
    PLUSONE = auto()
    REROLL = auto()
    IMMEDIATE =  auto()
    DECISION = auto()

@dataclass
class Bonus:
    type: BonusType
    color: Color = None
    value: int = None

