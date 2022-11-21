# RBI% Stat

How to calculate: RBI / RISP during PAs

For context, the average RBI% in 2021 was about 43.9%

Use calc_rbi_perc.py (function rbi_perc) to calculate it for any given player (or even the whole league) in the list of plays you provide. It returns `-1.0` when the player has no PAs, and a fraction between 0 and 1 to represent the percent (multiply by 100 to get the percent).

Credit for the idea of this stat to u/jkingsbery on Reddit

## Implementation notes

A player is rewarded for batting in a runner from first base as well as hitting homers. Because of this, you may see an RBI% that is >100% with small sample size hitters who hit a multi-run homer and have had no other RISP opportunities. Additionally, there will be a division by 0 error (-1.0 will be returned) if there hasn't been a RISP opportunity, even if the hitter hit a solo homer.

## Purpose

The purpose of this stat is to see how often a player takes advantage of RBI opportunities (being at bat with RISP).
This stat is supposed to be a better RBI: it is a rate stat which I generally prefer. It also benefits leadoff hitters who are less likely to get RISP during their at bats, and thus have low RBI numbers or even RBI/162 numbers.
