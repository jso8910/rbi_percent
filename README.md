# RBI% Stat

How to calculate: RBI / RISP during PAs

For context, the average RBI% in 2021 was about 43.9%

Use calc_rbi_perc.py (function rbi_perc) to calculate it for any given player (or even the whole league) in the list of plays you provide. It returns `-1.0` when the player has no PAs, and a fraction between 0 and 1 to represent the percent (multiply by 100 to get the percent).
