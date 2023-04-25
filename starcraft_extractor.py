import sys
from sc2reader.factories import SC2Factory
from os.path import join


def formatTeams(replay):
    teams = list()
    for team in replay.teams:
        players = list()
        for player in team:
            players.append("({0}) {1}".format(
                player.pick_race[0], player.name))
        formattedPlayers = '\n         '.join(players)
        teams.append("Team {0}:  {1}".format(team.number, formattedPlayers))
    return '\n\n'.join(teams)


def formatReplay(replay):
    return """{filename}
    --------------------------------------------
        SC2 Version {release_string}
    {category} Game, {start_time}
    {type} on {map_name}
    Length: {game_length}

    """.format(**replay.__dict__)


def main():
    sc2 = SC2Factory()
    replayUrl = "replays/firstRun/0dffaad1493241d3a281cbd1085c3bb6.SC2Replay"
    replay = sc2.load_replay(replayUrl)
    print(formatReplay(replay))
    print(formatTeams(replay))
    print("test")
    print(replay.filename)


if __name__ == "__main__":
    main()
