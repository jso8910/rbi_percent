import argparse
import sys
import os
from typing import Dict
import tqdm
import csv


def rbi_perc(plays: list[Dict[str, str]], player_id: str | None) -> float:
    """
    Returns the RBI% of a player.
    If player_id = None, returns the average RBI% of all players.
    """
    numerator = 0   # RBIs
    denominator = 0  # Total RISP in ABs
    for play in plays:
        if play["BAT_ID"] != player_id and player_id is not None:
            continue

        # If it isn't in these values, it isn't a finished PA. Otherwise some RISP will be double counted
        if not int(play["EVENT_CD"]) in [2, 3, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]:
            continue
        n_risp = 0
        if play["BASE2_RUN_ID"]:
            n_risp += 1
        elif play["BASE3_RUN_ID"]:
            n_risp += 1
        denominator += n_risp

        numerator += int(play["RBI_CT"])
    if denominator == 0:
        return -1.0
    return numerator / denominator


def main(start_year: int, end_year: int, player_id: str) -> float:
    if start_year > end_year:
        print("START_YEAR must be less than END_YEAR")
        sys.exit(1)
    elif start_year < 1915 or end_year > 2021:
        print("START_YEAR and END_YEAR must be between 1915 and 2021. If 2022 or a future year has been added to retrosheet, feel free to edit this file.")
        sys.exit(1)

    if not os.path.isdir("chadwick_csv"):
        print("The folder chadwick_csv doesn't exist. Have you run retrosheet_to_csv.sh?", file=sys.stderr)
        sys.exit(1)
    files = sorted(os.listdir("chadwick_csv"))
    if not len(files):
        print("The folder chadwick_csv doesn't have any folders. Have you run retrosheet_to_csv.sh?", file=sys.stderr)
        sys.exit(1)

    files = sorted(os.listdir("chadwick_csv"))
    files_filtered: list[str] = []
    for file in files:
        if int(file[0:4]) < start_year or int(file[0:4]) > end_year:
            continue
        else:
            files_filtered.append(file)
    plays: list[Dict[str, str]] = []

    for file in tqdm.tqdm(files_filtered):
        if int(file[0:4]) < start_year or int(file[0:4]) > end_year:
            continue
        file = "chadwick_csv/" + file
        with open(file, "r") as f:
            reader = csv.DictReader(f)
            plays.extend(list(reader))

    return rbi_perc(plays, player_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--player-id', '-p',
                        help="Retrosheet ID of the player you want to calculate the RBI% of", type=str, required=True)
    parser.add_argument('--start-year', '-s',
                        help="Start year of data gathering (defaults to 2000 for a somewhat reasonable default)", type=int, default=2000)
    parser.add_argument('--end-year', '-e',
                        help="End year of data gathering (defaults to 2021, current retrosheet year as of coding)", type=int, default=2021)

    args = parser.parse_args(sys.argv[1:])

    print(main(args.start_year, args.end_year, args.player_id))
