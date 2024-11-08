from functions import euclidean_distance, euclidean_distance_squared


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
        return min(sheep_herd, key=lambda sheep: euclidean_distance_squared(self._position, sheep.position) if sheep is not None else float('inf'))

    def move(self, target_sheep):
        x_wolf, y_wolf = self._position
        x_sheep, y_sheep = target_sheep.position
        wolf_sheep_distance = euclidean_distance(self._position, target_sheep.position)

        unit_vector = [(x_sheep - x_wolf) / wolf_sheep_distance, (y_sheep - y_wolf) / wolf_sheep_distance]
        x_wolf_change = unit_vector[0] * self._move_distance
        y_wolf_change = unit_vector[1] * self._move_distance

        self._position = (x_wolf + x_wolf_change, y_wolf + y_wolf_change)

    def act(self, sheep_herd):
        self._sated = False
        target_sheep = self.get_target(sheep_herd)
        target_sheep_index = sheep_herd.index(target_sheep)
        if euclidean_distance(self._position, target_sheep.position) <= self._move_distance:
            sheep_herd[target_sheep_index] = None
            self._position = target_sheep.position
            self._sated = True
        else:
            self.move(target_sheep)

        return target_sheep_index
