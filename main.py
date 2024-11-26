import json
import csv
import logging
import os.path

from argparse import ArgumentParser, ArgumentTypeError
from configparser import ConfigParser

from sheep import Sheep
from wolf import Wolf

logger = logging.getLogger(__name__)


def validate_ini_filename_argument(filename):
    if not filename.lower().endswith(".ini"):
        raise ArgumentTypeError("The configuration file must be an INI file.")
    if not os.path.isfile(filename):
        raise ArgumentTypeError("The configuration file doesn't exist.")
    return filename


def validate_positive_int_argument(value):
    if not value.lstrip("-").isdigit():
        raise ArgumentTypeError("The number must be an integer.")
    elif int(value) < 1:
        raise ArgumentTypeError("The number must be greater than zero.")
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
    parser.add_argument("-c", "--config", type=validate_ini_filename_argument, metavar="FILE",
                        help="An auxiliary configuration file, where %(metavar)s stands for a filename")
    parser.add_argument("-l", "--log", metavar="LEVEL",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Record events to a log, where %(metavar)s stands for a log level (DEBUG, INFO, WARNING, "
                             "ERROR, or CRITICAL)")
    parser.add_argument("-r", "--rounds", type=validate_positive_int_argument, default=50, metavar="NUM",
                        help="The maximum number of rounds, where %(metavar)s denotes an integer")
    parser.add_argument("-s", "--sheep", type=validate_positive_int_argument, default=15, metavar="NUM",
                        help="The number of sheep, where %(metavar)s denotes an integer")
    parser.add_argument("-w", "--wait", action="store_true",
                        help="Introduce a pause after displaying basic information about the status of the simulation "
                             "at the end of each round until a key is pressed")
    args = parser.parse_args()

    if args.log:
        logging.basicConfig(filename="chase.log", filemode="w", level=args.log)
    else:
        logging.disable(logging.CRITICAL)

    if args.config:
        config = ConfigParser()
        config.read(args.config)
        sheep_position_limit = get_positive_number_from_config(config, "Sheep", "InitPosLimit")
        sheep_move_distance = get_positive_number_from_config(config, "Sheep", "MoveDist")
        wolf_move_distance = get_positive_number_from_config(config, "Wolf", "MoveDist")
        logger.debug("The following values were loaded from %s: "
                     "Sheep Initial Position Limit (%s), Sheep Move Distance (%s), Wolf Move Distance (%s)",
                     args.config, sheep_position_limit, sheep_move_distance, wolf_move_distance)
    else:
        sheep_position_limit = 10.0
        sheep_move_distance = 0.5
        wolf_move_distance = 1.0

    max_rounds = args.rounds
    herd_size = args.sheep

    sheep_herd = [Sheep(sheep_position_limit, sheep_move_distance, seq_num) for seq_num in range(herd_size)]
    logger.info("Initial positions of all sheep were determined")

    wolf = Wolf(wolf_move_distance)

    animal_positions_by_round = []

    with open("alive.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["round", "alive_sheep"])

    for round_num in range(max_rounds):
        logger.info("Round %d started", round_num + 1)
        if not any(sheep_herd):
            logger.info("The simulation terminated - all sheep have been eaten")
            print("All sheep have been eaten.")
            return

        print(f"Round number: {round_num + 1}")
        for sheep in sheep_herd:
            if sheep is not None:
                sheep.move()

        logger.info("All alive sheep moved")

        target_sheep_index = wolf.act(sheep_herd)
        alive_sheep_number = len([sheep for sheep in sheep_herd if sheep is not None])

        print(f"Position of the wolf: {[round(num, 3) for num in wolf.position]}")
        print(f"Number of alive sheep: {alive_sheep_number}")
        if wolf.sated:
            print(f"The wolf ate sheep {target_sheep_index}")
        else:
            print(f"The wolf is chasing sheep {target_sheep_index}")

        logger.info("Number of alive sheep: %d", alive_sheep_number)
        print()

        animal_positions_by_round.append({
            "round_no": round_num + 1,
            "wolf_pos": wolf.position,
            "sheep_pos": [sheep.position if sheep is not None else None for sheep in sheep_herd]
        })

        with open("pos.json", "w", encoding="utf-8") as file:
            json.dump(animal_positions_by_round, file, indent=4)
            logger.debug("The position of each animal was saved to pos.json")

        with open("alive.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow([round_num + 1, alive_sheep_number])
            logger.debug("The round number and the number of alive sheep were saved to alive.csv")

        if args.wait:
            input("Press Enter to continue...")
            print()

    logger.info("The simulation terminated - predefined maximum number of rounds has been reached")


if __name__ == "__main__":
    main()
