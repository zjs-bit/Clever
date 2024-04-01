from abc import ABC, abstractmethod
import numpy as np
from enum import Enum, auto
from typing import List
from Bonus import Bonus,BonusType
from Color import Color
from Environment import *
from ActionTypes import DiceAction

class BoardArea(ABC):   
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def state(self) -> dict:
        """Returns state of the board area"""

    @abstractmethod
    def score(self) -> int:
        """Returns the current score of the board area"""

    def validate_color(self,dice_color: Color) -> bool:
        """Checks if the dice to be played is white or matches the color of the BoardArea"""
        return dice_color is self.color or dice_color is Color.WHITE
    
    @abstractmethod
    def validate_move(self, action: DiceAction) -> bool:
        """Checks if a given dice with color value can be scored in the board area given the current state.
        If applicable, considers the chosen placement coordinate in placement to ensure validity"""

    @abstractmethod
    def score_dice(self,action: DiceAction) -> None:
        """Scores a dice with value 'dice_value', color 'dice_color', at coordinates given by placement"""

    @abstractmethod
    def get_bonus(self,action: DiceAction = None) -> List[Bonus]:
        """Get applicable bonuses after a given dice is played, with details of placement in **kwargs"""
        
    @abstractmethod
    def fox_obtained(self) -> bool:
        """Checks whether the fox has been obtained in this board area"""

class VectArea(BoardArea):

    def __init__(self) -> None:
        super().__init__()
        self.last_filled: int = -1
        self.length:int = 11
        self.current_board: np.array = np.zeros(self.length)
        self.bonus_vect = None
        self.score_vect = None
        self.fox_position: int = 7

    def validate_move(self, action: DiceAction) -> bool:
        
        if not self.validate_color(action.color):
            return False
        
        elif self.last_filled == self.length - 1:
            #Board area filled
            return False
        
        else: return True

    def score(self) -> float:
        return np.dot(self.score_vect,self.current_board)
    
    def get_bonus(self):
        """Gets the bonus obtained from the last played dice"""
        return self.bonus_vect[self.last_filled]
    
    def fox_obtained(self) -> bool:
        return self.last_filled >= self.fox_position
    
class PurpleArea(VectArea):

    def __init__(self) -> None:
        super().__init__()
        
        self.color: Color = Color.PURPLE
        self.score_vect = np.ones(self.length)
        self.bonus_vect =  self.bonus_vect = self.bonus_vect = [Bonus(BonusType.NONE),
                           Bonus(BonusType.NONE),
                           Bonus(BonusType.NONE),
                           Bonus(BonusType.REROLL),
                           Bonus(BonusType.DECISION,Color.BLUE),
                           Bonus(BonusType.PLUSONE),
                           Bonus(BonusType.DECISION,Color.YELLOW),
                           Bonus(BonusType.NONE),
                           Bonus(BonusType.REROLL),
                           Bonus(BonusType.IMMEDIATE,Color.GREEN,1),
                           Bonus(BonusType.IMMEDIATE,Color.ORANGE,6),
                           Bonus(BonusType.PLUSONE)
                           ]

    def state(self) -> dict:
        return {'score':self.score(),
                'last_filled':self.last_filled,
                'last_filled_value': self.current_board[self.last_filled]}

    def score(self):
        return super().score()
    
    def validate_move(self, action: DiceAction) -> bool:
        if not super().validate_move(action):
            return False
        elif self.last_filled > -1 and action.value < self.current_board[self.last_filled] % 6:
            return False
        else:
            return True
        
    def score_dice(self, dice_value: int):
        self.last_filled += 1
        self.current_board[self.last_filled] = dice_value

    def fox_obtained(self) -> bool:
        return super().fox_obtained()

class OrangeArea(VectArea):

    def __init__(self) -> None:
        super().__init__()
        
        self.color:Color = Color.ORANGE
        self.score_vect = [i for i in range(self.length)]
        self.bonus_vect = [Bonus(BonusType.NONE),
                           Bonus(BonusType.NONE),
                           Bonus(BonusType.REROLL),
                           Bonus(BonusType.NONE),
                           Bonus(BonusType.DECISION,Color.YELLOW),
                           Bonus(BonusType.PLUSONE),
                           Bonus(BonusType.NONE),
                           Bonus(BonusType.NONE),
                           Bonus(BonusType.NONE),
                           Bonus(BonusType.IMMEDIATE,Color.PURPLE, value = 6),
                           Bonus(BonusType.NONE)
                           ]
        self.multipliers = np.array([1,1,1,2,1,1,2,1,2,1,3])
        self.fox_position = 8

    def state(self):
        return {'score': self.score,
                'last_filled': self.last_filled}
    
    def score(self):
        return super().score()
    
    def validate_move(self, action: DiceAction) -> bool:
        return super().validate_move(action)
    
    def score_dice(self, dice_value: int, dice_color: str) -> None:
        self.last_filled += 1
        self.current_board[self.last_filled] = dice_value*self.multipliers[self.last_filled]

    def fox_obtained(self) -> bool:
        return super().fox_obtained()

class GreenArea(VectArea):

    def __init__(self) -> None:
        super().__init__()
        
        self.color:Color = Color.GREEN
        self.score_vect = np.cumsum(np.array([1 + i+1 for i in range(self.length)]))
        self.bonus_vect = self.bonus_vect = \
                          [Bonus(BonusType.NONE),
                           Bonus(BonusType.NONE),
                           Bonus(BonusType.NONE),
                           Bonus(BonusType.PLUSONE),
                           Bonus(BonusType.NONE),
                           Bonus(BonusType.DECISION,Color.BLUE),
                           Bonus(BonusType.NONE),
                           Bonus(BonusType.NONE),
                           Bonus(BonusType.IMMEDIATE,Color.PURPLE,6),
                           Bonus(BonusType.REROLL),
                           Bonus(BonusType.NONE)]
        
        self.lower_bds = np.array([1,2,3,4,5,1,2,3,4,5,1])

    def state(self):
        return {'last_filled': self.last_filled}
    
    def score(self):
        return super().score()
    
    def validate_move(self, action: DiceAction) -> bool:
        return super().validate_move(action) and self.lower_bds[self.last_filled+1] <= action.value
    
    def score_dice(self) -> None:
        self.current_board[self.last_filled] = 0
        self.last_filled += 1
        self.current_board[self.last_filled] = 1

    def fox_obtained(self) -> bool:
        return super().fox_obtained()

class GridArea(BoardArea):
    def __init__(self,rows,columns) -> None:
        super().__init__()
        self.rows  = rows
        self.columns = columns
        self.current_board = np.zeros((rows,columns))
        self.fox_row = 0
        self.row_bonuses = None
        self.column_bonuses = None
        self.diag_bonus = None
        
    def validate_move(self, action: DiceAction) -> bool:
        color_chk = super().validate_color(action.color)
        return color_chk and self.current_board[action.placement] == 0
    
    def get_col_bonus(self,col: int) -> Bonus:
        if np.prod(self.current_board[:,col]) == 1:
            return self.column_bonuses[col]
        else:
            return Bonus(BonusType.NONE)
        
    def get_row_bonus(self,row:int) -> Bonus:
        if np.prod(self.current_board[row,:]) == 1:
            return self.row_bonuses[row]
        else:
            return Bonus(BonusType.NONE)
        
    def fox_obtained(self) -> bool:
        return np.prod(self.current_board[self.fox_row,:])==1
    
class BlueArea(GridArea):

    def __init__(self) -> None:
        super().__init__(3, 4)
        self.current_board[0,0] = 1
        self.scores: np.array = np.cumsum(np.array([1+i for i in range(11)]))
        self.color: Color = Color.BLUE
        self.fox_row:int = 3
        self.row_bonuses = [Bonus(BonusType.IMMEDIATE,Color.ORANGE,5),
                            Bonus(BonusType.DECISION,Color.YELLOW),
                            Bonus(BonusType.NONE)]
        self.column_bonuses = [Bonus(BonusType.REROLL),
                              Bonus(BonusType.IMMEDIATE,Color.GREEN,1),
                              Bonus(BonusType.IMMEDIATE,Color.PURPLE),
                              Bonus(BonusType.PLUSONE)]

    def state(self) -> dict:
        return {'board': np.reshape(self.current_board,self.rows*self.columns)}

    def score(self) -> int:
        sqs_filled = np.sum(self.current_board)
        return self.scores[sqs_filled - 1]

    def _get_placement(self,bluewhitesum: int)-> tuple:
        """Takes the played dice value 'dice_value' and the value of the unplayed white/blue dice 'wb_val'
        and returns the coordinates in the blue area corresponding with these values. 
        """
        row = int(np.floor((bluewhitesum-1)/self.columns))
        column = (bluewhitesum-1) % self.columns
        return  (row,column)
    
    def get_bonus(self, action: DiceAction) -> List[Bonus]:
        row,col = action.placement
        return (super().get_col_bonus(col),super().get_row_bonus(row))
    
    def validate_move(self, action: DiceAction) -> bool:
        return super().validate_move(action) and action.placement == self._get_placement(action.value)
    
    def score_dice(self, dice_value: int, bluewhitesum: int) -> None:
        self.current_board[self._get_placement(dice_value,bluewhitesum)] = 1

    def fox_obtained(self) -> bool:
        return super().fox_obtained()

class YellowArea(GridArea):
    def __init__(self) -> None:
        super().__init__(4, 4)
        self.color = Color.YELLOW
        self.current_board = np.fliplr(np.eye(self.rows,self.columns))
        self.fox_row: int = 4

        self.board_values = np.array([[3,6,5,0],
                                      [2,1,0,5],
                                      [1,0,2,4],
                                      [0,3,4,6]])
        
        self.column_scores = np.array([10,14,16,20])
        
        self.row_bonuses = [Bonus(BonusType.DECISION,Color.BLUE),
                            Bonus(BonusType.IMMEDIATE,Color.ORANGE,4),
                            Bonus(BonusType.IMMEDIATE,Color.GREEN,1),
                            Bonus(BonusType.NONE)]
        
        self.diag_bonus = Bonus(BonusType.PLUSONE)

    def state(self) -> dict:
        return {'board': self.current_board.flatten()}
    
    def score(self) -> int:
        return np.dot(np.prod(self.current_board,axis=0),self.column_scores)
    
    def validate_move(self, action: DiceAction) -> bool:
        return super().validate_move(action) and action.value == self.board_values[action.placement]

    def score_dice(self, placement: tuple) -> None:
        self.current_board[placement] = 1

    def fox_obtained(self) -> bool:
        return super().fox_obtained()
    
    def get_bonus(self,action:DiceAction) -> List[Bonus]:
        return (super().get_row_bonus(action.placement[0]),self.get_diag_bonus(action.placement[0]))
    
    def get_diag_bonus(self,placement) -> Bonus:
        if placement[0] == placement[1] and np.prod(np.diag(self.current_board)) == 1:
            return self.diag_bonus
        else:
            return Bonus(BonusType.NONE)

            
def main():
    pass


if __name__ == '__main__':
    main()

    