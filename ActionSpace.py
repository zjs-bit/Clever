from dataclasses import dataclass, field
from Color import Color
from typing import List, Dict, Tuple
from TurnStage import TurnStage
from Board import Board
from BoardComponents import BlueArea, YellowArea
from Dice import Dice
from ActionTypes import Action, DiceAction, StrategicAction
from Bonus import Bonus, BonusType


@dataclass
class ActionSpace:

    rolling_stages: Tuple[TurnStage] = (
        TurnStage.ROLL1,
        TurnStage.ROLL2,
        TurnStage.ROLL3,
    )
    
    decision_dice = [Color.BLUE, Color.YELLOW]

    dice_selections: List[DiceAction] = field(
        default_factory=lambda: [c for c in Color])

    yellow_placements: List[dict] =  field(default_factor = lambda: 
        [{'value': YellowArea().board_values[i,j], 'placement': (i, j)}
            for i in range(4)
            for j in range(4)
            if not i == 3 - j])

    blue_placements: List[DiceAction] = field(
        default_factory=lambda: [
            DiceAction(Color.BLUE, placement=BlueArea()._get_placement(i))
            for i in range(1, 13)
        ]
    )

    strat_actions: List[StrategicAction] = field(
        default_factory=lambda: [StrategicAction.REROLL, StrategicAction.PASS]
    )

    def __post_init__(self):
        self.white_actions = (
            [DiceAction(Color.WHITE, a.area) for a in self.gop_actions]
            + [
                DiceAction(Color.WHITE, a.area, a.value, a.placement)
                for a in self.yellow_actions
            ]
            + [
                DiceAction(Color.WHITE, a.area, a.value, a.placement)
                for a in self.blue_actions
            ]
        )
        self.dice_actions: List[DiceAction] = self.color_actions + self.white_actions
        self.dice_dict: dict[int, DiceAction] = {
            key: action for key, action in enumerate(self.dice_actions)
        }
        self.strat_dict: dict[int, StrategicAction] = {
            i + max(self.dice_dict.keys()): act
            for i, act in enumerate(self.strat_actions)
        }

        self.pass_dict: dict[int, StrategicAction] = {
            i: act for i, act in self.strat_dict.items() if act is StrategicAction.PASS
        }

    def get_valid_actions(
        self, stage: TurnStage, bonus_processing: bool, board: Board, dice: Dice
    ) -> Dict[int, Action]:

        if bonus_processing:
            dice_acts = self._valid_bonus_actions(board)

        else:

            if stage is TurnStage.SILVERTRAY:
                dice_acts = self._valid_silvertray(board, dice)

            elif stage in (TurnStage.ROLL1, TurnStage.ROLL2, TurnStage.ROLL3):
                dice_acts = self._valid_from_diceset(dice._free, board, dice.vals)

            elif stage is TurnStage.POSTROUND and board.plusones > 0:
                dice_acts = self._valid_from_diceset(dice.vals.keys(), board, dice.vals)

            elif stage is TurnStage.ROUND4:
                dice_acts = self._valid_round4_actions(board, dice.vals)

            else:
                raise ValueError(f"Unrecognized TurnStage: {stage}")

            dice_acts.update(self._valid_strategic(stage, board))

        return dice_acts
    
    def validate_action(self, act: Action, board: Board, dice: Dice, stage: TurnStage, asbonus: bool)-> bool:
        """
        Args:
            act (Action): an game action (Dice placement or Strategic)
            board (Board): a game board
            dice (Dice): the dice handler
            stage (TurnStage): the current game stage
            asbonus (bool): Whether the action is being played as a bonus action

        Returns:
            bool: True if Action act is currently feasible
        """
        
        if isinstance(act, StrategicAction):
            self._validate_strategic(act,board)
            
        elif isinstance(act, DiceAction):
            
            
        else:
            raise ValueError(f"act: Action type not recognized")
        
    def _attach_current_dice(self,dice_vals: Dict[Color, int]):
        for a in self.dice_dict.values():
            a.value = dice_vals[a.color]
            
    def _valid_from_diceset(
        self, diceset: List[Color], board: Board, dice_val: Dict[Color, int]
    ) -> Dict[int, DiceAction]:
        self._attach_current_dice(dice_val)
        return {
            i: act
            for i, act in self.dice_dict.items()
            if self._validate_dice_action(act, diceset, board)
        }

    def _validate_dice_action(
        self, action: DiceAction, diceset: List[Dice], board: Board
    ) -> bool:
        return action.color in diceset and board.areas[action.area].validate_move(
            action
        )
        
    def get_diceset(self, stage: TurnStage, bonus_processing: bool, dice: Dice)-> List[Color]:
        if bonus_processing:
            return  self.decision_dice
        else:
            if stage in  self.rolling_stages:
                return dice._free
            elif stage in TurnStage.SILVERTRAY:
                return  

    def _valid_bonus_actions(self, board: Board) -> Dict[int, DiceAction]:

        valid = {
            i: act
            for i, act in self.dice_dict.items()
            if act.color in board.pending_bonuses
            and board.areas[act.color].validate_move(act)
        }

        return valid

    def _valid_round4_actions(
        self, board: Board, dice_vals: Dict[Color, int]
    ) -> Dict[int, DiceAction]:
        self._attach_current_dice(dice_vals)
        return {
            i: act
            for i, act in self.dice_dict.items()
            if act.color is not Color.WHITE and board.areas[act.area].validate_move(act)
        }

    def _valid_silvertray(self, board: Board, dice: Dice) -> Dict[int, DiceAction]:
        silver_tray_valid = self._valid_from_diceset(dice._silvertray, board, dice.vals)

        if self._valid_from_diceset(dice._silvertray, board, dice.vals):
            # If a dice in the silver tray can be used
            return silver_tray_valid
        else:
            # Player can choose from the played dice
            return self._valid_from_diceset(dice._played, board, dice.vals)

    def _valid_strategic(
        self, stage: TurnStage, board: Board
    ) -> Dict[int, StrategicAction]:

        if stage in (self.rolling_stages) and board.rerolls > 0:
            return self.strat_dict
        else:
            return self.pass_dict

    def display(self, actions: Dict[int, Action]) -> List:
        for a in actions.values():
            a.print_action()


def main():
    # print(A.area)
    z = ActionSpace()
    b = Board()
    d = Dice()
    b.handle_bonus(Bonus(BonusType.DECISION, Color.BLUE))
    a = z.get_valid_actions(TurnStage.ROLL1, bonus_processing=True, board=b, dice=d)
    z.display(a)


if __name__ == "__main__":
    main()
