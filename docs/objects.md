# Objects module

## Quickstart

    from api import objects as obj

    obj.init(LEAGUE_API_KEY)
    champions = obj.Champion.load_list()
    for champ in champions:
        print '{0: <14} | ATK: {1: <10} | DEF: {2: <10} | MAG: {3: <10} | DIF: {4: <10}'.format(
            champ.name,
            '+' * champ.attack_rank ,
            '+' * champ.defense_rank,
            '+' * champ.magic_rank,
            '+' * champ.difficulty_rank
        )

## Full reference

    objects.init(api_key)

Initialize the module. Instantiates an API client with the right API key
in the background. **Needed before performing any other operation**

    class objects.Dto

Base class for the data objects in the module

### Champion

    class objects.Champion

Instances represent a champion Dto.

    static objects.Champion.load_list(free_to_play=false, region='na')

Retrieve a list of champions available in the given `region`. If `free_to_play`
is set to `True`, only champions that are currently in the free-to-play rotation
will be retrieved.

### Game

    class objects.Game

Instances represent a game Dto.

* `fellow_players` attribute is populated with `Player` instances
* `statistics` attribute is populated with `RawStat` instances

------
    static objects.Game.load_recent_games(summoner_id, region='na')

Retrieve a list of the most recent games for the given `summoner_id` in the
given `region`.

### Player

    class objects.Player

Instances represent a player Dto.

    objects.Player#get_summoner()

Retrieve the summoner associated with this player object.
Note that this method will perform an API call that will count against your
rate limits.

### Summoner

    class objects.Summoner

Instances represent a summoner Dto.

    static objects.Summoner.load_summoner(summoner_id, region='na')

Retrieve the summoner identified by the given `summoner_id` in that `region`.

    static objects.Summoner.load_summoner_by_name(name, region='na')

Retrieve a summoner by its summoner `name` in the given `region`

### League

    class objects.League

Instances represent a League Dto.

* `entries` attribute is populated with `LeagueItem` instances

-----
    static objects.load_summoner_leagues(summoner_id, region='na')

Retrieve the leagues associated with the summoner identified by `summoner_id`
in the given `region`. Result is a map with one entry for each team and each
queue the summoner is ranked in. Key is team ID or summoner ID (if solo queue),
value is a `League` instance.

    class objects.LeagueItem

Instances represent a LeagueItem Dto.

* `mini_series` is a `MiniSeries` instance if present, `None` otherwise

### PlayerStatsSummary

    class objects.PlayerStatsSummary

Instances represent a PlayerStatsSummary Dto.

* `aggregated_stats` attribute is populated with `AggregatedStat` instances


### RankedStats

    class objects.RankedStats

Instances represent a RankedStats Dto.

* `champions` atribute is populated with `ChampionStats` instances

------
    static objects.RankedStats.load_ranked_stats(summoner_id, season=None, region='na')

Retrieve ranked stats for the given `summoner_id` in the given `region`.
`season` defaults to the current season, accepted values are
`"SEASON3"`, `"SEASON4"`.

    objects.RankedStats#get_summoner()

Retrieve the summoner associated with these stats.
Note that this method will perform an API call that will count against your
rate limits.

    objects.RankedStats#get_all_champion_stats()

Get a map containing all the associated `ChampionStats` instances.
Keys are champion names and champion IDs, values are `ChampionStats` instances.

    objects.RankedStats#get_champion_stats(champion_id)

Find the ChampionStats object for the given `champion_id`

    objects.RankedStats#get_champion_stats_by_name(name):

Find the ChampionStats object for the given champion `name`

    class ChampionStats(Dto)

Instances represent a ChampionStats Dto.

* `stats` attribute is populated with `ChampionStat` instances

### MasteryPage

    class objects.MasteryPage

Instances represent a MasteryPage Dto.

* `talents` attribute is populated with `Talent` instances

-------
    static objects.MasteryPage.load_summoner_masteries(summoner_id, region='na')

Retrieve all mastery pages for the summoner identified by `summoner_id`
in the given `region`.

### RunePage

    class objects.RunePage

Instances represent a RunePage Dto.

* `slots` attribute is populated with `RuneSlot` instances

-------
    static objects.RunePage.load_rune_pages(summoner_id, region='na')

Retrieve all rune pages for the summoner identified by `summoner_id`
in the given `region`.

    objects.RunePage#get_runes(self)

Retrieve all the `Rune` instances present associated with this rune page.

    class objects.RuneSlot

* `rune` attribute is a `Rune` instance

### Team

    class objects.Team

Instances represent a Team Dto.

* `match_history` attribute is populated with `MatchSummary` instances

---------
    static objects.Team.load_summoner_teams(summoner_id, region='na')

Retrieve all the teams of which `summoner_id` in the given `region` is a member.

    objects.Team#get_message_of_the_day()

Return a tuple containing

* The update date of the team's MOTD
* The version of the message
* The message itself

---------
    objects.Team#get_roster(self):

Return a list of `TeamMemberInfo` instances for this team.

    objects.Team#get_team_id(self):

Return the team ID
