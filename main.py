import json
import csv

from argparse import ArgumentParser

from sheep import Sheep
from wolf import Wolf


def main():
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", nargs=1, metavar="FILE",
                        help="An auxiliary configuration file, where %(metavar)s stands for a filename")
    parser.add_argument("-l", "--log", nargs=1, metavar="LEVEL",
                        help="Record events to a log, where %(metavar)s stands for a log level - DEBUG(10), INFO(20), "
                             "WARNING(20), ERROR(20), or CRITICAL(50)")
    parser.add_argument("-r", "--rounds", nargs=1, default=50, metavar="NUM",
                        help="The maximum number of rounds, where %(metavar)s denotes an integer")
    parser.add_argument("-s", "--sheep", nargs=1, default=15, metavar="NUM",
                        help="The number of sheep, where %(metavar)s denotes an integer;")
    parser.add_argument("-w", "--wait", action="store_true",
                        help="Introduce a pause after displaying basic information about the status of the simulation "
                             "at the end of each round until a key is pressed")
    args = parser.parse_args()

    max_rounds = 50
    herd_size = 15
    wolf_move_distance = 1.0
    sheep_move_distance = 0.5
    position_limit = 10.0

    sheep_herd = [Sheep(position_limit, sheep_move_distance) for _ in range(herd_size)]
    wolf = Wolf(wolf_move_distance)

    animal_positions_by_round = []
    alive_sheep_number_by_round = []

    for round_num in range(max_rounds):
        if not any(sheep_herd):
            print("All sheep have been eaten.")
            break

        print(f"Round number: {round_num + 1}")
        for sheep in sheep_herd:
            if sheep is not None:
                sheep.move()

        target_sheep_index = wolf.act(sheep_herd)
        alive_sheep_number = len([sheep for sheep in sheep_herd if sheep is not None])

        print(f"Position of the wolf: {[round(num, 3) for num in wolf.position]}")
        print(f"Number of alive sheep: {alive_sheep_number}")
        if wolf.sated:
            print(f"The wolf ate a sheep at index {target_sheep_index}")
        else:
            print(f"The wolf is chasing a sheep at index {target_sheep_index}")

        print()

        animal_positions_by_round.append({
            "round_no": round_num + 1,
            "wolf_pos": wolf.position,
            "sheep_pos": [sheep.position if sheep is not None else None for sheep in sheep_herd]
        })

        alive_sheep_number_by_round.append(alive_sheep_number)

    # TODO: Save the data to the files after every round
    with open("pos.json", "w", encoding="utf-8") as file:
        json.dump(animal_positions_by_round, file, indent=4)

    with open("alive.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["round_no", "alive_sheep_no"])
        for round_no, alive_sheep_no in enumerate(alive_sheep_number_by_round, 1):
            writer.writerow([round_no, alive_sheep_no])


if __name__ == "__main__":
    main()