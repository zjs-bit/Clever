from dataclasses import dataclass, field
from Color import Color
from typing import List
from TurnStage import TurnStage
from Board import Board
from BoardComponents import BlueArea
from Dice import Dice
from ActionTypes import DiceAction,StrategicAction

@dataclass
class ActionSpace:
    gop_actions: List[DiceAction] = field(
        default_factory = lambda: [DiceAction(c) for c in Color if c in (Color.ORANGE,Color.GREEN,Color.PURPLE)])
    
    yellow_actions: List[DiceAction] = field(
        default_factory = lambda: [DiceAction(Color.YELLOW, placement = (i,j)) for i in range(4) for j in range(4) if not i == 3-j])
    
    blue_actions: List[DiceAction] = field(
        default_factory= lambda: [DiceAction(Color.BLUE, placement = BlueArea()._get_placement(i)) for i in range(1,13)])

    strat_actions: List[StrategicAction] = field(
        default_factory = lambda: [StrategicAction.REROLL, StrategicAction.PASS])
    
    def __post_init__(self):
        self.color_actions = self.gop_actions + self.yellow_actions + self.blue_actions
        self.white_actions = [DiceAction(Color.WHITE,a.area) for a in self.gop_actions] + [DiceAction(Color.WHITE,a.area,a.value,a.placement) for a in self.yellow_actions] + [DiceAction(Color.WHITE,a.area,a.value,a.placement) for a in self.blue_actions]
        self.dice_actions: List[DiceAction] = self.color_actions + self.white_actions
        self.dice_dict: dict = {key:action for key,action in enumerate(self.dice_actions)}
        self.strat_dict: dict = {i + max(self.dice_dict.keys()):act for i,act in enumerate(self.strat_actions)}

    def get_valid_actions(self,stage:TurnStage,board: Board, dice: Dice):
        if stage is TurnStage.SILVERTRAY:
            return self._valid_from_diceset(dice._silvertray ,board, dice.vals)
        elif stage in (TurnStage.ROLL1, TurnStage.ROLL2, TurnStage.ROLL3):
            return self._valid_from_diceset(dice._free, board, dice.vals).update(self.strat_dict)
        elif stage is TurnStage.BONUS:
            return self._valid_bonus_actions(board)
        elif stage is TurnStage.POSTROUND:
            return self._valid_plusone_actions(board, dice.vals)

    def _valid_from_diceset(self,diceset:List[Color],board: Board, dice_val: dict) -> List[DiceAction]:
        self._attach_current_dice(dice_val)
        return {i:act for i,act in self.dice_dict.items()\
                if self._validate_dice_action(act,diceset,board)}

    def  _validate_dice_action(self,action: DiceAction, diceset: List[Dice],board: Board):
       return action.color in diceset and board.areas[action.area].validate_move(action)

    def _attach_current_dice(self,dice: dict):
        for k,act in self.dice_dict.items():
            act.value = dice[Color.WHITE] + dice[Color.BLUE] if act.area is Color.BLUE else dice[act.color]

    def _valid_plusone_actions(self, board: Board, dice_val: dict) -> List[DiceAction]:
        if board.plus_ones > 0:
            return self._valid_from_diceset(dice_val.keys(),board,dice_val)
        else:
            return []

    def _valid_bonus_actions(self, board: Board) -> List[DiceAction]:

        valid = []
        if Color.YELLOW in board.pending_bonuses:
            valid += self.yellow_actions

        if Color.BLUE in board.pending_bonuses:
            valid += self.blue_actions

        return valid
    
    def display(self,actions: dict) -> List:
        print([f"{a.color.name} dice in {a.area.name}; value: {a.value}{'; placement:' + str(a.placement) if a.placement is not None else ''}" for a in actions.values()])
        


def main():
    A = DiceAction(Color.BLUE)
    #print(A.area)
    z = ActionSpace()
    b=Board()
    dice = Dice()
    dice.roll()
    print(z.display(z._valid_from_diceset(dice._free,b,dice.vals)))
    print(dice.all)

if __name__ == '__main__':
    main()