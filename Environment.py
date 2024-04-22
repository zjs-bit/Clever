from Dice import Dice
from Player import Player
from TurnStage import TurnStage
from typing import List
from ActionTypes import Action, StrategicAction


class GameEnvironment:

    def __init__(self, players: List[Player]) -> None:
        self.dice: Dice = Dice()
        self.stage: TurnStage = TurnStage.ROLL1
        self.bonus_processing: bool = False
        self.players = players
        self.curr_player: Player = players[0]
        self.player_num: int = 0
        self.nplayers: int = len(players)
        self.round: int = 1
        self.nrounds: int = min(6, 6 - self.nplayers + 2)

    def state(self) -> dict:
        """Returns the game state in dictionary form"""
        return {
            "rd": self.round,
            "stage": self.stage,
            "currplayer": self.player_num,
            "board": self.players[0].board.state(),
        }

    def advance(self, last_action: Action):
        # Check for bonuses that must be processed:
        if self.curr_player.board.pending_bonuses:
            self.bonus_processing = True

        else:
            self.bonus_processing = False

            if self.stage is TurnStage.ROLL1:
                self.stage = TurnStage.ROLL2

            elif self.stage is TurnStage.ROLL2:
                self.stage = TurnStage.ROLL3

            elif self.stage is TurnStage.ROLL3:
                self.dice.finalize_silver_tray()
                self.stage = TurnStage.SILVERTRAY

            elif self.stage is TurnStage.SILVERTRAY:
                self._advance_player()
                if self.player_num == 0:
                    self.stage = TurnStage.POSTROUND

            elif self.stage is TurnStage.SILVERTRAY:
                self._advance_player()
                if self.player_num == 0:
                    self.stage = TurnStage.POSTROUND

            elif self.stage is TurnStage.POSTROUND:
                self._advance_from_postround(last_action)

            elif self.stage is TurnStage.ROUND4:
                self._advance_player()
                if self.player_num == 0:
                    self.stage = TurnStage.ROLL1

            else:
                raise ValueError(f"Stage: {self.stage} not recognized")

    def _advance_from_postround(self, last_action: Action):
        if last_action is StrategicAction.PASS or self.curr_player.board.plusones == 0:
            self._advance_player()
            if self.player_num == 0:
                self.round += 1
                if self.round == 4:
                    self.stage = TurnStage.ROUND4
                    self.dice.set_round4_vals()
                elif self.round > self.nrounds:
                    self.stage = TurnStage.GAMEOVER
                else:
                    self.stage = TurnStage.ROLL1

        else:
            pass

    def _advance_player(self) -> None:
        self.player_num = (self.player_num + 1) % self.nplayers
        self.curr_player = self.players[self.player_num]
