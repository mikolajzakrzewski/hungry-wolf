import random
import logging


logger = logging.getLogger(__name__)


class Sheep:
    def __init__(self, position_limit, move_distance, sequence_number):
        self._position = tuple(random.uniform(position_limit * -1, position_limit) for _ in range(2))
        logger.debug("Sheep %d was generated at position %s", sequence_number, self._position)
        self._move_distance = move_distance
        self._sequence_number = sequence_number

    @property
    def position(self):
        return self._position

    @property
    def move_distance(self):
        return self._move_distance

    @property
    def sequence_number(self):
        return self._sequence_number

    def move(self):
        moves = {'LEFT': (self._position[0] - self._move_distance, self._position[1]),
                 'RIGHT': (self._position[0] + self._move_distance, self._position[1]),
                 'UP': (self._position[0], self._position[1] + self._move_distance),
                 'DOWN': (self._position[0], self._position[1] - self._move_distance)}
        direction = random.choice(list(moves.keys()))
        logger.debug("Sheep %d will move %s", self._sequence_number, direction)
        self._position =  moves[direction]
        logger.debug("Sheep %d moved to position %s", self._sequence_number, self._position)
