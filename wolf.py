import logging

from functions import euclidean_distance, euclidean_distance_squared

logger = logging.getLogger(__name__)

class Wolf:
    def __init__(self, move_distance):
        self._position = (0.0, 0.0)
        self._move_distance = move_distance
        self._sated = False

    @property
    def position(self):
        return self._position

    @property
    def move_distance(self):
        return self._move_distance

    @property
    def sated(self):
        return self._sated

    def get_target(self, sheep_herd):
        target = min(sheep_herd,
                     key=lambda sheep: euclidean_distance_squared(
                         self._position, sheep.position
                     ) if sheep is not None else float('inf'))
        logger.debug("The wolf is closest to sheep %s with distance to it equal to %s",
                     target.sequence_number, euclidean_distance(self._position, target.position))
        return target

    def move(self, target_sheep):
        x_wolf, y_wolf = self._position
        x_sheep, y_sheep = target_sheep.position
        wolf_sheep_distance = euclidean_distance(self._position, target_sheep.position)

        unit_vector = [(x_sheep - x_wolf) / wolf_sheep_distance, (y_sheep - y_wolf) / wolf_sheep_distance]
        x_wolf_change = unit_vector[0] * self._move_distance
        y_wolf_change = unit_vector[1] * self._move_distance

        self._position = (x_wolf + x_wolf_change, y_wolf + y_wolf_change)
        logger.info("The wolf moved")
        logger.debug("Wolf position: %s", self._position)

    def act(self, sheep_herd):
        self._sated = False
        target_sheep = self.get_target(sheep_herd)
        target_sheep_index = target_sheep.sequence_number
        if euclidean_distance(self._position, target_sheep.position) <= self._move_distance:
            sheep_herd[target_sheep_index] = None
            logger.info("Sheep %s was eaten", target_sheep_index)
            self._position = target_sheep.position
            self._sated = True
        else:
            logger.info("The wolf is chasing sheep %s", target_sheep_index)
            self.move(target_sheep)

        return target_sheep_index
