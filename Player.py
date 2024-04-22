from dataclasses import dataclass
from Board import Board
from ActionSpace import ActionSpace
from TurnStage import TurnStage
from ActionTypes import Action, DiceAction, StrategicAction
from Dice import Dice
from typing import Dict
import random


@dataclass
class Player:
    """Stores information about a player and executes the gameplay for the individual"""

    id: int
    name: str = ""
    board: Board = Board()

    def _execute_strategic(self, action: StrategicAction, dice: Dice):

        if action is StrategicAction.PASS:
            pass
        elif action is StrategicAction.REROLL:
            dice.roll()
        else:
            raise ValueError("StrategicAction action not of recognized type")

    def _execute_feasible(self, action: DiceAction):
        self.board.score_dice(action)

    def _post_dict_action(
        self, action: DiceAction, stage: TurnStage, bonus_flag: bool
    ) -> None:

        if bonus_flag:
            # We just used a bonus
            self.board.pending_bonuses.remove(action.color)

        else:
            if stage is TurnStage.POSTROUND:
                # Plus one used
                self.board.plusones -= 1

    def execute_action(
        self, action: Action, dice: Dice, stage: TurnStage, bonus_flag: bool
    ) -> None:
        if isinstance(action, DiceAction):
            self._execute_feasible(action)
            self._post_dict_action(action, stage, bonus_flag)

        else:
            self._execute_strategic(action, dice)

    def get_feasible_actions(
        self, action_handler: ActionSpace, stage: TurnStage, bonuses: bool, dice: Dice
    ) -> Dict[int, Action]:
        return action_handler.get_valid_actions(stage, bonuses, self.board, dice)

    def choose_action(self, feasible_actions: Dict[int, Action]) -> Action:
        return random.choice(list(feasible_actions.values()))

    def get_reward(self) -> int:
        return self.board.get_reward()
