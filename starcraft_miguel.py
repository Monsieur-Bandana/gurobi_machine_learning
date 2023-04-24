import sc2reader

replay = sc2reader.load_replay(
    "replays/0dffaad1493241d3a281cbd1085c3bb6.SC2Replay")

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

    marines = []
    for event in replay.events:
        if event.name == "UnitBornEvent" and event.control_pid == player_id:
            if (event.unit.name == "Marine"):
                marines.append(event.unit)

        if event.name == "UnitDiedEvent":
            if (event.unit.name == "Marine"):
                marines.remove(event.unit)

        if event.second > second:
            break

    return len(marines)


workers_1 = [worker_counter(replay, k, 1) for k in range(300)]
marines_1 = [marines_counter(replay, k, 1) for k in range(300)]
workers_2 = [worker_counter(replay, k, 2) for k in range(300)]
marines_2 = [marines_counter(replay, k, 2) for k in range(300)]

print("{} setzte {} worker und {} marines in den ersten 300 sekunden ein".format(
    replay.players[0], workers_1[len(workers_1)-1], marines_1[len(marines_1)-1]))

print("{} setzte {} worker und {} marines in den ersten 300 sekunden ein".format(
    replay.players[1], workers_2[len(workers_2)-1], marines_2[len(marines_2)-1]))
