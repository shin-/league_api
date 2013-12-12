import six

import client
import utils

c = None

def init(api_key):
    global c
    c = client.Client(api_key)


class Dto(object):
    def __init__(self, dct, region='na'):
        self._source_dict = dct
        self._region = region
        for k, v in six.iteritems(dct):
            self.__dict__[utils.camel_to_underscore(k)] = v

    def __unicode__(self):
        shown_attributes = [x for x in self.__dict__.keys() if x[0] != '_']
        s = u'League API {0} [{2}] ({1})'.format(
            self.__class__.__name__,
            ', '.join(shown_attributes),
            self._region
        )
        if len(s) > 128:
            s = s[:127] + '...)'
        return s

    def __str__(self):
        return unicode(self).encode('utf-8')

class Champion(Dto):
    @classmethod
    def load_list(cls, free_to_play=False, region='na'):
        return [cls(x) for x in c.get_champions(free_to_play, region)['champions']]

    def __unicode__(self):
        return u'League API Champion [{2}] ({0}, {1})'.format(
            self.id, self.name, self._region
        )


class Game(Dto):
    def __init__(self, dct, region='na'):
        super(Game, self).__init__(dct, region)
        self.fellow_players = [Player(x, self._region) for x in self.fellow_players]
        self.statistics = [RawStat(x) for x in self.statistics]

    @classmethod
    def load_recent_games(cls, summoner_id, region='na'):
        return [cls(x, region) for x in c.get_recent_games(summoner_id, region)['games']]

    def __unicode__(self):
        return u'League API Game [{2}] ({0}, {1})'.format(
            self.game_id, self.game_mode, self._region
        )

class Player(Dto):
    def get_summoner(self):
        return Summoner(c.get_summoner(self.summoner_id, self._region))


class RawStat(Dto):
    def __unicode__(self):
        return u'League API RawStat ({0}, {1} = {2})'.format(
            self.id, self.name, self.value
        )


class Summoner(Dto):
    @classmethod
    def load_summoner(cls, summoner_id, region='na'):
        return cls(c.get_summoner(summoner_id, region))

    @classmethod
    def load_summoner_by_name(cls, name, region='na'):
        return cls(c.get_summoner_by_name(name, region))

    def __unicode__(self):
        return u'League API Summoner [{2}] ({0}, {1})'.format(
            self.id, self.name, self._region
        )


class League(Dto):
    def __init__(self, dct, region='na'):
        super(League, self).__init__(dct, region)
        self.entries = [LeagueItem(x, region) for x in self.entries]

    @classmethod
    def load_summoner_leagues(cls, summoner_id, region='na'):
        leagues_map = c.get_summoner_leagues(summoner_id, region)
        for k, v in six.iteritems(leagues_map):
            leagues_map[k] = cls(v, region)
        return leagues_map

    def __unicode__(self):
        return u'League API League [{3}] ({0}, {1}, {2})'.format(
            self.name, self.queue, self.tier, self._region
        )


class LeagueItem(Dto):
    def __init__(self, dct, region='na'):
        super(LeagueItem, self).__init__(dct, region)
        if getattr(self, 'mini_series', None):
            self.mini_series = MiniSeries(self.mini_series, region)

    def __unicode__(self):
        return u'League API LeagueItem [{2}] ({0}, {1})'.format(
            self.player_or_team_id, self.player_or_team_name, self._region
        )

class MiniSeries(Dto):
    pass


class PlayerStatsSummary(Dto):
    def __init__(self, dct, region='na'):
        super(PlayerStatsSummary, self).__init__(dct, region)
        self.aggregated_stats = [
            AggregatedStat(x, region) for x in self.aggregated_stats
        ]

    @classmethod
    def load_stats_summary(cls, summoner_id, season=None, region='na'):
        return [
            cls(x, region) for x in c.get_stats_summary(
                            summoner_id,
                            season,
                            region
                        )['playerStatSummaries']
        ]


class AggregatedStat(Dto):
    def __unicode__(self):
        return u'League API AggregatedStat [{3}] ({0}, {1} = {2})'.format(
            self.id, self.name, self.count, self._region
        )


class RankedStats(Dto):
    def __init__(self, dct, region='na'):
        super(RankedStats, self).__init__(dct, region)
        self.champions = [ChampionStats(x, region) for x in self.champions]

    @classmethod
    def load_ranked_stats(cls, summoner_id, season=None, region='na'):
        return cls(c.get_ranked_stats(summoner_id, season, region), region)

    def get_summoner(self):
        return Summoner(c.get_summoner(self.summoner_id, self._region))

    def get_all_champion_stats(self):
        result = {}
        for stats in self.champions:
            lst = stats.stats
            result[stats.id] = lst
            result[stats.name] = lst
        return result

    def get_champion_stats(self, champion_id):
        result = [x for x in self.champions if x.id == champion_id]
        if len(result) == 0:
            return None
        return result[0].stats

    def get_champion_stats_by_name(self, name):
        name = name.lower()
        result = [x for x in self.champions if x.name.lower() == name]
        if len(result) == 0:
            return None
        return result[0].stats


class ChampionStats(Dto):
    def __init__(self, dct, region='na'):
        super(ChampionStats, self).__init__(dct, region)
        self.stats = [ChampionStat(x, region) for x in self.stats]
        if not getattr(self, 'name', None):
            self.name = ''

    def __unicode__(self):
        return u'League API ChampionStats [{2}] ({0}, {1})'.format(
            self.id, self.name, self._region
        )


class ChampionStat(Dto):
    def __unicode__(self):
        return u'League API ChampionStat ({0}, {1} = {2})'.format(
            self.id, self.name, self.value
        )


class MasteryPage(Dto):
    def __init__(self, dct, region='na'):
        super(MasteryPage, self).__init__(dct, region)
        self.talents = [Talent(x) for x in self.talents]

    @classmethod
    def load_summoner_masteries(cls, summoner_id, region='na'):
        return [cls(x) for x in c.get_summoner_masteries(summoner_id, region)['pages']]


class Talent(Dto):
    def __unicode__(self):
        return u'League API Talent ({0}, {1}, {2})'.format(
            self.id, self.name, self.rank
        )


class RunePage(Dto):
    def __init__(self, dct, region='na'):
        super(RunePage, self).__init__(dct, region)
        if getattr(self, 'slots', None):
            self.slots = [RuneSlot(x) for x in self.slots]
        else:
            self.slots = None

    @classmethod
    def load_rune_pages(cls, summoner_id, region='na'):
        return [cls(x) for x in c.get_summoner_runes(summoner_id, region)['pages']]

    def get_runes(self):
        if not self.slots:
            return None
        return [x.rune for x in self.slots]


class RuneSlot(Dto):
    def __init__(self, dct, region='na'):
        super(RuneSlot, self).__init__(dct, region)
        self.rune = Rune(self.rune)

class Rune(Dto):
    def __unicode__(self):
        return u'League API Rune ({0}, {1}, {2})'.format(
            self.id, self.name, self.tier
        )


class Team(Dto):
    def __init__(self, dct, region='na'):
        super(Team, self).__init__(dct, region)
        self.match_history = [MatchSummary(x) for x in self.match_history]

    @classmethod
    def load_summoner_teams(cls, summoner_id, region='na'):
        return [cls(x) for x in c.get_summoner_teams(summoner_id, region)]

    def get_message_of_the_day(self):
        return (
            self.message_of_day['createDate'],
            self.message_of_day['version'],
            self.message_of_day['message']
        )

    def get_roster(self):
        return [TeamMemberInfo(x) for x in self.roster['memberList']]

    def get_team_id(self):
        return self.team_id['fullId']


class MatchSummary(Dto):
    pass

class TeamMemberInfo(Dto):
    pass