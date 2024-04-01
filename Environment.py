from Dice import Dice
from Player import Player
from TurnStage import TurnStage
from typing import List

class GameEnvironment:
    
    def __init__(self, players: List[Player]) -> None:
        self.Dice = Dice()
        self.stage = TurnStage.ROLL1
        self.players = players
        self.curr_player = players[0]
        self.player_num = 0
        self.n_players = len(players)
        self.rounds = 6 - self.n_players + 2

    def advance(self):
        
        #Check for bonuses that must be processed:
        if self.curr_player.board.check_pending_bonuses(): 
            self.stage = TurnStage.BONUS

        else:
            if self.stage is TurnStage.ROLL1:
                self.stage = TurnStage.ROLL2

            elif self.stage is TurnStage.ROLL2:
                self.stage = TurnStage.ROLL3 

            elif self.stage is TurnStage.ROLL3:
                self.Dice.finalize_silver_tray()
                self.stage = TurnStage.SILVERTRAY 

            elif self.stage is TurnStage.SILVERTRAY:
                self._advance_player()
                if self.player_num == 0:
                     self.stage = TurnStage.POSTROUND

            elif self.stage is TurnStage.SILVERTRAY:
                self._advance_player()
                if self.player_num == 0: self.stage = TurnStage.POSTROUND

            elif self.stage is TurnStage.POSTROUND:
                self._advance_player()
                if self.player_num == 0:
                    self.round +=1
                    if self.round == 4:
                        self.stage = TurnStage.ROUND4
                    else: self.stage = TurnStage.ROLL1
        
    def _advance_player(self) -> None:
        self.player_num = (self.player_num + 1) % self.n_players
        self.curr_player = self.curr_player[self.player_num]