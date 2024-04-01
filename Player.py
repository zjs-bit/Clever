from dataclasses import dataclass
from Board import *
from Action import *
from TurnStage import TurnStage
import random

@dataclass
class Player:
    """Stores information about a player and executes the gameplay for the individual"""

    id: int
    name: str = ''
    board: Board = Board()

    def _execute_strategic(self,action: StrategicAction, dice: Dice):
        if action is StrategicAction.REROLL:
            dice.roll()
        else:
            raise ValueError("StrategicAction action not of recognized type")

    def _execute_feasible(self, action: DiceAction):
        with self.board.areas[action.color] as area:  
            area.score_dice(action)
            bonuses = area.get_bonus(action)

        self.board.handle_bonus(bonuses)

    def get_feasible_actions(self, action_handler: ActionSpace, stage: TurnStage, dice: Dice) -> dict:
        return action_handler.get_valid_actions(stage,self.board,dice)
    
    def get_random_action(self,feasible_actions: dict): 
        return random.choice([feasible_actions.values()])