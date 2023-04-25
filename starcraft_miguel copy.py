import sc2reader
import matplotlib.pyplot as plt
import numpy as np

replay = sc2reader.load_replay(
    "replays/firstRun/0a5d5a0d30434374a8b68439eb77e8e6.SC2Replay")


def worker_counter(replay, second, player_id):
    workers = []
    for event in replay.events:
        if event.name == "UnitBornEvent" and event.control_pid == player_id:
            if event.unit.is_worker:
                workers.append(event.unit)

        if event.name == "UnitDiedEvent":
            if event.unit in workers:
                workers.remove(event.unit)

        if event.second > second:
            break

    return len(workers)


def total_unit_counter(replay, second, player_id):
    units = []
    for event in replay.events:
        if event.name == "UnitBornEvent" and event.control_pid == player_id:

            units.append(event.unit)

        if event.name == "UnitDiedEvent":
            if event.unit in units:
                units.remove(event.unit)

        if event.second > second:
            break

    return len(units)


def get_time_of_first_max_supply():
    length_of_game = replay.frames // 24
    units_1 = [total_unit_counter(replay, k, 1) for k in range(length_of_game)]

    maxunits = 0
    second = 0
    maxSec = 0
    for unitcount in units_1:
        if unitcount > maxunits:
            maxunits = unitcount
            maxSec = second
        second = second + 1

    return maxSec


"""
print(maxunits)

print("maxunits for-loop:" + str(maxunits) +
      ", maxSec: " + str(maxSec) + " second: "+str(second)+" arrayLen: " + str(len(units_1)))

plt.figure()
plt.plot(workers_1, label=replay.players[0])
plt.plot(workers_2, label=replay.players[1])
plt.legend(loc=2)
plt.show()
"""
