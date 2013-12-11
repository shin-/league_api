import six

import client


c = None

def init(api_key):
    global c
    c = client.Client(api_key)


class Dto(object):
    def __init__(self, dct, region='na'):
        self.id = dct.get('id', None)
        self._source_dict = dct
        self._region = region

    def __getattr__(self, attr):
        return self._source_dict[attr]


class Champion(Dto):
    def __init__(self, dct):
        super(Champion, self).__init__(dct)

    @classmethod
    def load_list(cls, free_to_play=False, region='na'):
        return [cls(x) for x in c.get_champions(free_to_play, region)['champions']]


class Game(Dto):
    @classmethod
    def load_recent_games(cls, summoner_id, region='na'):
        return [cls(x, region) for x in c.get_recent_games(summoner_id, region)['games']]

    def get_fellow_players(self):
        return [Player(x, self._region) for x in self.fellowPlayers]

    def get_stats(self):
        return [RawStat(x) for x in self.statistics]


class Player(Dto):
    def get_summoner(self):
        return Summoner(c.get_summoner(self.summonerId, self._region))


class RawStat(Dto):
    pass


class Summoner(Dto):
    @classmethod
    def load_summoner(cls, summoner_id, region='na'):
        return cls(c.get_summoner(summoner_id, region))

    @classmethod
    def load_summoner_by_name(cls, name, region='na'):
        return cls(c.get_summoner_by_name(name, region))


class League(Dto):
    @classmethod
    def load_summoner_leagues(cls, summoner_id, region='na'):
        leagues_map = c.get_summoner_leagues(summoner_id, region)
        for k, v in six.iteritems(leagues_map):
            leagues_map[k] = cls(v)
        return leagues_map

    def get_league_items(self):
        return [LeagueItem(x) for x in self.entries]


class LeagueItem(Dto):
    def get_miniseries(self):
        return MiniSeries(self.miniseries)


class MiniSeries(Dto):
    pass


class PlayerStatsSummary(Dto):
    @classmethod
    def load_stats_summary(cls, summoner_id, season=None, region='na'):
        return [
            cls(x) for x in c.get_stats_summary(
                            summoner_id,
                            season,
                            region
                        )['playerStatsSummaries']
        ]

    def get_aggregated_stats(self):
        return [AggregatedStat(x) for x in self.aggregatedStats]


class AggregatedStat(Dto):
    pass


class RankedStats(Dto):
    @classmethod
    def load_ranked_stats(cls, summoner_id, season=None, region='na'):
        return cls(c.get_ranked_stats(summoner_id, season, region), region)

    def get_summoner(self):
        return Summoner(c.get_summoner(self.summonerId, self._region))

    def get_all_champion_stats(self):
        result = {}
        for stats in self.champions:
            lst = [ChampionStat(x) for x in stats['stats']]
            result[stats['id']] = lst
            result[stats['name']] = lst
        return result

    def get_champion_stats(self, champion_id):
        result = [x for x in self.champions if x['id'] == champion_id]
        if len(result) == 0:
            return None
        return [ChampionStat(x) for x in result[0]['stats']]

    def get_champion_stats_by_name(self, name):
        name = name.lower()
        result = [x for x in self.champions if x['name'].lower() == name]
        if len(result) == 0:
            return None
        return [ChampionStat(x) for x in result[0]['stats']]


class ChampionStat(Dto):
    pass


class MasteryPage(Dto):
    @classmethod
    def load_summoner_masteries(cls, summoner_id, region='na'):
        return [cls(x) for x in c.get_summoner_masteries(summoner_id, region)['pages']]

    def get_talents(self):
        return [Talent(x) for x in self.talents]


class Talent(Dto):
    pass


class RunePage(Dto):
    @classmethod
    def load_rune_pages(cls, summoner_id, region='na'):
        return [cls(x) for x in c.get_summoner_runes(summoner_id, region)['pages']]

    def get_runes(self):
        return [Rune(x['rune']) for x in self.slots]


class Rune(Dto):
    pass


class Team(Dto):
    @classmethod
    def load_summoner_teams(cls, summoner_id, region='na'):
        return [cls(x) for x in c.get_summoner_teams(summoner_id, region)]

    def get_match_history(self):
        return [MatchSummary(x) for x in self.matchHistory]

    def get_message_of_the_day(self):
        return (
            self.messageOfDay['createDate'],
            self.messageOfDay['version'],
            self.messageOfDay['message']
        )

    def get_roster(self):
        return [TeamMemberInfo(x) for x in self.roster['memberList']]

    def get_team_id(self):
        return self.teamId['fullId']


class MatchSummary(Dto):
    pass
