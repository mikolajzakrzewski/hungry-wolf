import json
import csv

from argparse import ArgumentParser, ArgumentTypeError
from configparser import ConfigParser

from sheep import Sheep
from wolf import Wolf


def ini_filename_valid(filename):
    if not filename.lower().endswith(".ini"):
        raise ArgumentTypeError("The configuration file must be an INI file.")
    return filename


def positive_int_valid(value):
    if not value.lstrip("-").isdigit():
        raise ArgumentTypeError("The number of rounds must be an integer.")
    elif int(value) < 1:
        raise ArgumentTypeError("The number of rounds must be greater than zero.")
    return int(value)


def get_positive_number_from_config(config, section, option):
    value = config.get(section, option)
    if not value.lstrip("-").replace(".", "", 1).isdigit():
        raise ValueError(
            f"Option '{option}' in section '{section}' of the config file must be a number. Provided: {value}"
        )
    elif float(value) <= 0:
        raise ValueError(
            f"Option '{option}' in section '{section}' of the config file must be greater than zero. Provided: {value}"
        )
    return float(value)


def main():
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", type=ini_filename_valid, metavar="FILE",
                        help="An auxiliary configuration file, where %(metavar)s stands for a filename")
    parser.add_argument("-l", "--log", metavar="LEVEL",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Record events to a log, where %(metavar)s stands for a log level (DEBUG, INFO, WARNING, "
                             "ERROR, or CRITICAL)")
    parser.add_argument("-r", "--rounds", type=positive_int_valid, default=50, metavar="NUM",
                        help="The maximum number of rounds, where %(metavar)s denotes an integer")
    parser.add_argument("-s", "--sheep", type=positive_int_valid, default=15, metavar="NUM",
                        help="The number of sheep, where %(metavar)s denotes an integer;")
    parser.add_argument("-w", "--wait", action="store_true",
                        help="Introduce a pause after displaying basic information about the status of the simulation "
                             "at the end of each round until a key is pressed")
    args = parser.parse_args()

    if args.config:
        config = ConfigParser()
        config.read(args.config)
        sheep_position_limit = get_positive_number_from_config(config, "Sheep", "InitPosLimit")
        sheep_move_distance = get_positive_number_from_config(config, "Sheep", "MoveDist")
        wolf_move_distance = get_positive_number_from_config(config, "Wolf", "MoveDist")
    else:
        sheep_position_limit = 10.0
        sheep_move_distance = 0.5
        wolf_move_distance = 1.0

    if args.log:
        # TODO: Implement logging with the specified level
        pass
    else:
        # TODO: Implement logging with the specified level
        pass

    max_rounds = args.rounds
    herd_size = args.sheep

    sheep_herd = [Sheep(sheep_position_limit, sheep_move_distance) for _ in range(herd_size)]
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

        # TODO: The task mentions pressing any key to continue instead of just enter, correct if necessary
        if args.wait:
            input("Press any key to continue...")

    # TODO: Save the data at the end of every round, not just at the end of the simulation, if necessary
    with open("pos.json", "w", encoding="utf-8") as file:
        json.dump(animal_positions_by_round, file, indent=4)

    with open("alive.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["round_no", "alive_sheep_no"])
        for round_no, alive_sheep_no in enumerate(alive_sheep_number_by_round, 1):
            writer.writerow([round_no, alive_sheep_no])


if __name__ == "__main__":
    main()