import sc2reader
import pandas as pd
import shutil

dataset = []

"""


replay = sc2reader.load_replay(
    "replays/0dffaad1493241d3a281cbd1085c3bb6.SC2Replay")

"""


def worker_counter(replay, second, player_id):
    workers = 0

    for event in replay.events:
        if event.name == "UnitBornEvent" and event.control_pid == player_id:

            if event.unit.is_worker:
                workers = workers + 1

        if event.name == "UnitDiedEvent":

            if event.unit.is_worker:
                workers = workers - 1

        if event.second > second:
            break

    return workers


def army_counter(replay, second, player_id):

    marines = 0
    for event in replay.events:
        if event.name == "UnitBornEvent" and event.control_pid == player_id:
            if (event.unit.is_army):
                marines = marines + 1

        if event.second > second:
            break

    return marines


def marines_counter(replay, second, player_id):

    marines = 0
    for event in replay.events:
        if event.name == "UnitBornEvent" and event.control_pid == player_id:
            if (event.unit.name == "Marine"):
                marines = marines + 1

        if event.second > second:
            break

    return marines


def forEachReplay(replay):

    for player in replay.players:
        if ((str(player) in str(replay.winner))):
            workers = worker_counter(replay, 600, player.pid)
            marines = army_counter(replay, 600, player.pid)

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
    print("step {} of {}".format(step, 341))

finaldata = pd.DataFrame(dataset).to_csv(
    "csv_dateien/sc2.csv", header=["player", "total_workers", "total_marines"])

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
