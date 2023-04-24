import sc2reader
import matplotlib.pyplot as plt

replay = sc2reader.load_replay(
    "replays/0dffaad1493241d3a281cbd1085c3bb6.SC2Replay")


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


length_of_game = replay.frames // 24
workers_1 = [worker_counter(replay, k, 1) for k in range(length_of_game)]
workers_2 = [worker_counter(replay, k, 2) for k in range(length_of_game)]

plt.figure()
plt.plot(workers_1, label=replay.players[0])
plt.plot(workers_2, label=replay.players[1])
plt.legend(loc=2)
plt.show()
