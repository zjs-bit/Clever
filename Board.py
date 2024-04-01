from Bonus import *
from Color import Color
from BoardComponents import *

class Board:
    """Keeps track of the board and game state"""
    def __init__(self) -> None:
        self.orange: BoardArea = OrangeArea()
        self.purple: BoardArea = PurpleArea()
        self.green: BoardArea = GreenArea()
        self.blue: BoardArea = BlueArea()
        self.yellow: BoardArea = YellowArea()
        self.round: int = 1
        self.rerolls: int = 1
        self.plus_ones: int = 0
        self.areas = {Color.YELLOW: self.yellow,
                       Color.BLUE: self.blue,
                       Color.GREEN: self.green,
                       Color.ORANGE: self.orange,
                       Color.PURPLE: self.purple}
        self.pending_bonuses = []

    def state(self):
        return {'rerolls':self.rerolls,
                'plus_ones':self.plus_ones,
                Color.YELLOW: self.yellow.state(),
                Color.BLUE: self.blue.state(),
                Color.GREEN: self.green.state(),
                Color.ORANGE: self.orange.state(),
                Color.PURPLE: self.purple.state()}
    
    def handle_bonus(self,*bonus: Bonus) -> None:
        for b in bonus:
            if b.type is BonusType.NONE:
                pass
            elif b.type is BonusType.REROLL:
                    self.board.rerolls += 1
            elif b.type is BonusType.PLUSONE:
                    self.board.plusones += 1
            elif b.type is BonusType.DECISION:
                    self.pending_bonuses.append(b)
            elif b.type is BonusType.IMMEDIATE:
                    self.board.score_immediate_bonus(b)
            else:
                raise TypeError("Unexpected Bonus Type")

    def score_immediate_bonus(self,bonus:Bonus) -> None:
        if bonus.Type is not BonusType.IMMEDIATE:
             raise ValueError("Bonus type is not IMMEDIATE")
        else:
            board_area = self.board_areas[bonus.color]
            board_area.score_dice(bonus.value)

    def check_pending_bonuses(self):
         return len(self.pending_bonuses) > 0