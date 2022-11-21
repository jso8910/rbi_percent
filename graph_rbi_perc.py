import matplotlib.pyplot as plt  # type: ignore
import os
import csv
from calc_rbi_perc import rbi_perc
import tqdm
from typing import Dict
import sys

print("Note. The dependencies for this aren't in requirements.txt.")

files = sorted(os.listdir("downloads"))
files_filtered: list[str] = []
for file in files:
    # if file.endswith(".ROS"):
    #     print(file)
    if file.endswith(".ROS") and file[3:7] == "2021":
        files_filtered.append("downloads/" + file)

players: list[Dict[str, str]] = []
for file in files_filtered:
    with open(file, "r") as f:
        reader = csv.reader(f)
        for line in reader:
            players.append({"pid": line[0], "pname": line[2] + " " + line[1]})

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
    if int(file[0:4]) != 2021:
        continue
    else:
        files_filtered.append(file)
plays: list[Dict[str, str]] = []

for file in tqdm.tqdm(files_filtered):
    if int(file[0:4]) != 2021:
        continue
    file = "chadwick_csv/" + file
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        plays.extend(list(reader))

rbi_percs: list[Dict[str, str | float]] = []
for player in tqdm.tqdm(players):
    pa_count = 0
    for play in plays:
        if play["BAT_ID"] != player['pid']:
            continue
        pa_count += 1

    if pa_count > 162*3.1:
        rbi_percs.append({"pname": player["pname"], "pid": player["pid"], "RBI%": rbi_perc(
            plays, player["pid"]) * 100})


plt.bar(range(50), [p['RBI%'] for p in sorted(  # type: ignore
    rbi_percs, key=lambda x: x['RBI%'], reverse=True)][:50])
plt.xticks(range(50), [p['pname'] for p in sorted(  # type: ignore
    rbi_percs, key=lambda x: x['RBI%'], reverse=True)][:50], rotation=90, fontsize=7)
plt.xlabel("Name")  # type: ignore
plt.ylabel("RBI%")  # type: ignore
plt.title("Top 50 RBI\% leaders, 2021")  # type: ignore
plt.show()  # type: ignore
