import sc2reader
import pandas as pd
import shutil

dataset = []


def unit_counter(replay, second, player_id):
    workers = []
    for event in replay.events:
        if event.name == "UnitBornEvent" and event.control_pid == player_id:

            workers.append(event.unit)

        if event.name == "UnitDiedEvent":

            workers.remove(event.unit)

        if event.second > second:
            break

    return workers


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


def marines_counter(replay, second, player_id):
    workers = []
    for event in replay.events:
        if event.name == "UnitBornEvent" and event.control_pid == player_id:
            if (event.unit.name == "Marine"):
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


def get_time_of_first_max_supply(player):
    length_of_game = replay.frames // 24
    units_1 = [total_unit_counter(replay, k, player.pid)
               for k in range(length_of_game)]

    maxunits = 0
    second = 0
    maxSec = 0
    for unitcount in units_1:
        if unitcount > maxunits:
            maxunits = unitcount
            maxSec = second
        second = second + 1

    return maxSec


def forEachReplay(replay):

    for player in replay.players:
        if ((str(player.pick_race[0]) == "T") & (str(player) in str(replay.winner))):
            time = get_time_of_first_max_supply(player)
            workers = worker_counter(replay, time, player.pid)
            marines = marines_counter(replay, time, player.pid)

            dataset.append([player.name, workers, marines])
        """
        else:
            src = str(replay.filename)
            file = src.replace("replays/firstRun/", "")
            dest = ("replays/not_interesting/"+file)
            shutil.move(src, dest)
        """


step = 0


for replay in sc2reader.load_replays("replays/firstRun"):
    forEachReplay(replay)
    step = step + 1
    print("step {} of {}".format(step, 421))

finaldata = pd.DataFrame(dataset).to_csv(
    "csv_dateien/sc.csv", header=["player", "total_workers", "total_marines"])

print(finaldata)

"""


marines_1 = [marines_counter(replay, k, 1) for k in range(300)]
workers_2 = [worker_counter(replay, k, 2) for k in range(300)]
marines_2 = [marines_counter(replay, k, 2) for k in range(300)]

print("{} setzte {} worker und {} marines in den ersten 300 sekunden ein".format(
    replay.players[0], workers_1[len(workers_1)-1], marines_1[len(marines_1)-1]))

print("{} setzte {} worker und {} marines in den ersten 300 sekunden ein".format(
    replay.players[1], workers_2[len(workers_2)-1], marines_2[len(marines_2)-1]))

"""
