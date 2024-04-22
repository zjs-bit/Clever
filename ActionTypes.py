from dataclasses import dataclass
from Color import Color
from enum import Enum, auto
from typing import Protocol


class Action(Protocol):
    def print_action(self):
        pass


@dataclass
class DiceAction:
    color: Color
    area: Color = None
    value: int = None
    placement: tuple = None

    def __post_init__(self):
        if self.color is not Color.WHITE:
            self.area = self.color

    def print_action(self):
        print(
            f"Play {self.color.name} in {self.area.name}, value: {self.value}, {'placement:' + str(self.placement) if self.placement else ''}"
        )


class StrategicAction(Enum):
    # Only 1 in this version of clever
    REROLL = auto()
    PASS = auto()

    def print_action(self):
        print(f"Strategic action: {self.name}")
