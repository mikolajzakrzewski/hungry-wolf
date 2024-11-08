import random


class Sheep:
    def __init__(self, position_limit, move_distance):
        self._position = tuple(random.uniform(position_limit * -1, position_limit) for _ in range(2))
        self._move_distance = move_distance

    @property
    def position(self):
        return self._position

    @property
    def move_distance(self):
        return self._move_distance

    def move(self):
        moves = {'L': (self._position[0] - self._move_distance, self._position[1]),
                 'R': (self._position[0] + self._move_distance, self._position[1]),
                 'U': (self._position[0], self._position[1] + self._move_distance),
                 'D': (self._position[0], self._position[1] - self._move_distance)}
        self._position =  moves[random.choice(list(moves.keys()))]
