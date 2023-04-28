import os
import sc2reader
import pandas as pd
import shutil


def counter(replay, second, player_id):
    workers = []
    army = []
    armyValue = 0
    for event in replay.events:
        if event.name == "UnitBornEvent" and event.control_pid == player_id:
            if event.unit.is_worker:
                workers.append(event.unit)
            if event.unit.is_army:
                army.append(event.unit)
                armyValue = armyValue + event.unit.minerals + event.unit.vespene

        if event.name == "UnitDiedEvent":
            if event.unit in workers:
                workers.remove(event.unit)
            if event.unit in army:
                army.remove(event.unit)
                armyValue = armyValue - event.unit.minerals - event.unit.vespene

        if event.second > second:
            break

    return [len(workers), armyValue, len(army)]


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

    return [maxSec, maxunits]


dataset = []


def forEachReplay(replay):
    players = []
    armymax = []
    for player in replay.players:
     #   if (str(player.pick_race[0]) == "T"):
        firstLoop = get_time_of_first_max_supply(player)
        time = firstLoop[0]
        units = counter(replay, time, player.pid)
        workers = units[0]
        armyValue = units[1]
        armymax.append(armyValue/time)
        unitsNr = units[2]
        fraction = str(player.pick_race[0])
        winner = 0
        if str(player) in str(replay.winner):
            winner = 1
        players.append([player.name, workers, armyValue, unitsNr, time,
                       fraction, winner, replay.filename])

    maxV = 0
    loopStart = 0
    pitch = 0
    for x in armymax:
        if x > maxV:
            maxV = x
            pitch = loopStart
        loopStart = loopStart + 1

    players[pitch].append(1)
    for player in players:
        if len(player) < 9:
            player.append(0)
        dataset.append(player)


"""
        else:
            src = str(replay.filename)
            file = src.replace("replays/firstRun", "")
            file = file.replace("`\`", "")
            dest = str("replays/not_interesting/" + str(file))
            print(file)
            shutil.move(src, dest)
"""


step = 0
replayUrl = "replays/testRun"

for replay in sc2reader.load_replays(replayUrl):

    forEachReplay(replay)
    step = step + 1
    print("step {} of {}".format(step, len(os.listdir(replayUrl))))

finaldata = pd.DataFrame(dataset).to_csv(
    "csv_dateien/starcraftFinalcsvs/testRun.csv", header=["player", "total_workers", "total_army_value", "total_army", "time", "fraction", "winner", "replay_filename", "greater_army"])

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
