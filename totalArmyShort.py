import os
import sc2reader
import pandas as pd
import shutil

# Hier werden sämtliche "Events" einer Replaydatei innerhalb eines zeitlich festgelegten Rahmens. In diesem Fall handelt es sich bei den Events um die Zahl gesammelter Ressourcen,
# die Zahl hergestellter Worker Units und Army Units. Die Army und Worker Units werden in eine Liste gelegt. Stirbt die Unit bis zum gewählten Zeitpunkt, wird sie wieder aus
# der Liste entfernt


def counter(replay, second, player_id):
    workers = []
    army = []
    armyValue = 0
    armySupply = 0
    collectedMinerals = 0
    supply = 0
    for event in replay.events:

        if event.name == "PlayerStatsEvent" and player_id == event.pid:
            supply = event.food_made
            collectedMinerals = collectedMinerals + \
                event.minerals_current + event.vespene_current
        if event.name == "UnitBornEvent" and event.control_pid == player_id:
            if event.unit.is_worker:
                workers.append(event.unit)
            if event.unit.is_army:
                army.append(event.unit)
                armyValue = armyValue + event.unit.minerals + event.unit.vespene
                armySupply = armySupply + event.unit.supply

        if event.name == "UnitDiedEvent":
            if event.unit in workers:
                workers.remove(event.unit)
            if event.unit in army:
                army.remove(event.unit)
                armyValue = armyValue - event.unit.minerals - event.unit.vespene
                armySupply = armySupply - event.unit.supply
        if event.second > second:
            break

    return [len(workers), armyValue, armySupply, collectedMinerals, supply]

# Diese Schleife zählt alle Einheiten die ein Spieler in einer Partie produziert hat. Zuvor wurden sowohl diese Schleifentätigkeit,
# als auch die vorhergehende in derselben Schleife erledigt, Es wurde aberfestgestellt, dass das Programm schneller ist, wenn man diese
# und die vorhergehende Schleife voneinander trennt.


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

# Diese Schleife iteriert durch jedes Sekunde einer Partie und stellt fest, zu welchem Zeitpunkt ein Spieler seine größte Armee hat


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

    for player in replay.players:
     #   if (str(player.pick_race[0]) == "T"):
        firstLoop = get_time_of_first_max_supply(player)
        time = firstLoop[0]
        units = counter(replay, time, player.pid)
        workers = units[0]
        armyValue = units[1]
        unitsNr = units[2]
        collectedMinerals = units[3]
        supply = units[4]
        fraction = str(player.pick_race[0])
        winner = 0
        if str(player) in str(replay.winner):
            winner = 1

        dataset.append([player.name, workers, collectedMinerals, armyValue, unitsNr, supply, time,
                       fraction, winner, replay.filename])


step = 0
# Die Replays wurden in Datenpakete aus ca. 400 Replays aufgeteilt. Die Url wird nach jedem Duchlauf händisch geändert. Ein Durchlauf dauert ca. 20 Minuten
replayUrl = "replays/1stRun"

for replay in sc2reader.load_replays(replayUrl):

    forEachReplay(replay)
    step = step + 1
    print("step {} of {}".format(step, len(os.listdir(replayUrl))))

finaldata = pd.DataFrame(dataset).to_csv(
    "csv_dateien/starcraftFinalcsvs/1stRunSup.csv", header=["player", "total_workers", "resource_mining", "total_army_value", "total_army", "supply", "time", "fraction", "winner", "replay_filename"])

print(finaldata)
