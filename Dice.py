# Class for managing the dice in a game of the That's Pretty Clever"

from Color import Color
import numpy as np


class Dice:
    def __init__(self) -> None:
        self.vals = {c: np.random.randint(1, 7) for c in Color}
        self._free = list(self.vals.keys())
        self._silvertray = []
        self._played = []

    def _view_dice(self, *color: Color) -> int:
        return {c.name: self.vals[c] for c in color}

    @property
    def all(self):
        return self._view_dice(*self.vals.keys())

    @property
    def silvertray(self):
        return self._view_dice(*self._silvertray)

    @property
    def free(self):
        return self._view_dice(*self._free)

    @property
    def played(self):
        return self._view_dice(*self._played)

    def _reset(self) -> None:
        self = self.__init__()

    def roll(self) -> None:
        for color in self._free:
            self.vals[color] = np.random.randint(1, 7)

    def manage_after_play(self, played: Color) -> None:
        """Manages the dice after a player's selection during a turn"""

        self._played.append(played)
        self._free.remove(played)
        for c in self._free:
            if self.vals[c] < self.vals[played]:
                self._silvertray.append(c)
                self._free.remove(c)

    def finalize_silver_tray(self, nplayers: int = 1):
        """Finalizes the silver tray after completion of a turn"""

        if nplayers == 1:
            self._reset()
            self.roll()
            sorted_colors = sorted(self.vals, key=self.vals.get)
            self._silvertray = sorted_colors[:3]
            self._free = sorted_colors[3:]

        else:
            self._silvertray.append(self._free)

    def set_round4_vals(self):
        """Set's dice to optimal values for round 4 bonus actions"""

        self.vals[Color.ORANGE] = 6
        self.vals[Color.PURPLE] = 6
        self.vals[Color.GREEN] = 6


def main():
    g = Dice()
    print(g.all)


if __name__ == "__main__":
    main()
