import matplotlib.pyplot as plt  # type: ignore
import matplotlib.ticker as mtick  # type: ignore
import os
import csv
from calc_rbi_perc import rbi_perc
import tqdm
from typing import Dict
import sys

print("Note. The dependencies for this aren't guaranteed to be in requirements.txt.")

START_YEAR = 2000
END_YEAR = 2021

if not os.path.isdir("chadwick_csv"):
    print("The folder chadwick_csv doesn't exist. Have you run retrosheet_to_csv.sh?", file=sys.stderr)
    sys.exit(1)
files = sorted(os.listdir("chadwick_csv"))
if not len(files):
    print("The folder chadwick_csv doesn't have any folders. Have you run retrosheet_to_csv.sh?", file=sys.stderr)
    sys.exit(1)

files = sorted(os.listdir("chadwick_csv"))
rbi_percs: list[float] = []
for year in tqdm.tqdm(range(START_YEAR, END_YEAR + 1)):
    files_filtered: list[str] = []
    for file in files:
        if int(file[0:4]) != year:
            continue
        else:
            files_filtered.append(file)
    plays: list[Dict[str, str]] = []

    for file in files_filtered:
        if int(file[0:4]) != year:
            continue
        file = "chadwick_csv/" + file
        with open(file, "r") as f:
            reader = csv.DictReader(f)
            plays.extend(list(reader))

    rbi_percs.append(rbi_perc(plays, None) * 100)
print(rbi_percs)
xpoints = range(START_YEAR, END_YEAR + 1)
ypoints = rbi_percs

ax = plt.scatter(xpoints, ypoints, s=2).axes  # type: ignore
plt.plot(xpoints, ypoints, '-')   # type: ignore
plt.xlabel("Year")  # type: ignore
plt.ylabel("RBI%")  # type: ignore
plt.title("League RBI% by year")  # type: ignore
ax.set_ylim(0.0, 100.0)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())  # type: ignore
plt.show()  # type: ignore
