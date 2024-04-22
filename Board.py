from Bonus import Bonus, BonusType
from Color import Color
from BoardComponents import *
from typing import Dict


class Board:
    """Keeps track of the board and game state"""

    def __init__(self) -> None:

        self.orange: BoardArea = OrangeArea()
        self.purple: BoardArea = PurpleArea()
        self.green: BoardArea = GreenArea()
        self.blue: BoardArea = BlueArea()
        self.yellow: BoardArea = YellowArea()

        self.rerolls: int = 1
        self.plusones: int = 0
        self.areas: dict[Color, BoardArea] = {
            Color.YELLOW: self.yellow,
            Color.BLUE: self.blue,
            Color.GREEN: self.green,
            Color.ORANGE: self.orange,
            Color.PURPLE: self.purple,
        }
        self.pending_bonuses: List[Bonus] = []
        self.current_score: int = 0

    def state(self) -> dict:
        return {
            "rerolls": self.rerolls,
            "plus_ones": self.plusones,
            Color.YELLOW.name: self.yellow.state(),
            Color.BLUE.name: self.blue.state(),
            Color.GREEN.name: self.green.state(),
            Color.ORANGE.name: self.orange.state(),
            Color.PURPLE.name: self.purple.state(),
        }

    def _get_area_scores(self) -> Dict[Color, int]:
        return {c: a.score() for c, a in self.areas.items()}

    def score_areas(self) -> int:
        """Returns the current board score"""
        return sum(self._get_area_scores().values())

    def min_area_score(self) -> int:
        return min(self._get_area_scores().values())

    def score_foxes(self) -> int:
        """Returns the fox score for the current board"""
        nfoxes = sum([a.fox_obtained() for a in self.areas.values()])
        return nfoxes * self.min_area_score()

    def final_score(self) -> int:
        return self.score_areas() + self.score_foxes()

    def get_reward(self) -> int:

        new_score = self.score_areas()
        reward = new_score - self.current_score
        self.current_score = new_score

        return reward

    def score_dice(self, action: DiceAction) -> int:
        """Applies a dice action in the applicable area, processes immediate bonuses, and returns the reward"""

        self.areas[action.area].score_dice(
            dice_value=action.value, placement=action.placement
        )
        bonuses = self.areas[action.area].get_bonus(action)

        # Handle pending bonuses
        self.handle_bonus(*bonuses)

    def handle_bonus(self, *bonus: Bonus) -> None:
        for b in bonus:
            if b.type is BonusType.NONE:
                pass
            elif b.type is BonusType.REROLL:
                self.rerolls += 1
            elif b.type is BonusType.PLUSONE:
                self.plusones += 1
            elif b.type is BonusType.DECISION:
                self.pending_bonuses.append(b.color)
            elif b.type is BonusType.IMMEDIATE:
                self.score_immediate_bonus(b)
            else:
                raise TypeError("Unexpected Bonus Type")

    def score_immediate_bonus(self, bonus: Bonus) -> None:
        if bonus.type is not BonusType.IMMEDIATE:
            raise ValueError("Bonus type is not IMMEDIATE")
        else:
            self.areas[bonus.color].score_dice(dice_value=bonus.value)


def main():
    b = Board()


if __name__ == "__main__":
    main()
