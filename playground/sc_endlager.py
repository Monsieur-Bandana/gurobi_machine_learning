import sc2reader
import pandas as pd

dataset = []

replay = sc2reader.load_replay(
    "replays/firstRun/0dffaad1493241d3a281cbd1085c3bb6.SC2Replay")


event_names = set([event.name for event in replay.events])
# print(event_names)

events_of_type = {name: [] for name in event_names}
for event in replay.events:
    events_of_type[event.name].append(event)
#    print(event.name)


unit_born_events = events_of_type["UnitBornEvent"]
unit_died_events = events_of_type["UnitDiedEvent"]

marines = 0
scvs = 0

for ube in unit_born_events:

    unitName = str(ube.unit).split()[0]
    if (unitName == "Marine"):
        marines = marines + 1
    if (unitName == "SCV"):
        scvs = scvs + 1
    if (ube.second > 500):
        break

for ube in unit_died_events:
    unitName = str(ube.unit).split()[0]
    if (unitName == "Marine"):
        marines = marines - 1
    if (unitName == "SCV"):
        scvs = scvs - 1
    if (ube.second > 500):
        break

print(replay.winner)
print(replay.players[0])

src = str(replay.filename)
file = src.replace("replays/firstRun/", "")
print(src + " " + file)
dest = ("replays/not_interesting/"+file)
print(dest)
