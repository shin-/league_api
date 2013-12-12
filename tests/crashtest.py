import os
import time

import api.objects as api

summoner_id = 25196834

api.init(os.environ['LEAGUE_API_KEY'])

champions = api.Champion.load_list()
print unicode(champions[27])

recent = api.Game.load_recent_games(summoner_id, 'euw')
print unicode(recent[3])
print unicode(recent[3].fellow_players[2])
print unicode(recent[3].statistics[0])
print unicode(recent[3].fellow_players[2].get_summoner())

summoner = api.Summoner.load_summoner(summoner_id, 'euw')
print unicode(summoner)
summoner2 = api.Summoner.load_summoner_by_name('shinzer0', 'euw')
print unicode(summoner2)

print '### Mandatory pause (rate limit) ###'
time.sleep(10)

leagues_map = api.League.load_summoner_leagues(summoner_id, 'euw')
league = leagues_map.values()[0]
print unicode(league)
for entry in league.entries:
    print unicode(entry)

summary = api.PlayerStatsSummary.load_stats_summary(summoner_id, 'SEASON3', 'euw')
for summ in summary:
    for stat in summ.aggregated_stats:
        print unicode(stat)

ranked = api.RankedStats.load_ranked_stats(summoner_id, 'SEASON3', 'euw')
print unicode(ranked)
for stat in ranked.get_champion_stats_by_name('shyvana'):
    print unicode(stat)

masteries = api.MasteryPage.load_summoner_masteries(summoner_id, 'euw')
print unicode(masteries[3])
for talent in masteries[0].talents:
    print unicode(talent)

runes = api.RunePage.load_rune_pages(summoner_id, 'euw')
print unicode(runes[9])
for rune in runes[9].get_runes():
    print unicode(rune)

print '### Mandatory pause (rate limit) ###'
time.sleep(10)

teams = api.Team.load_summoner_teams(summoner_id, 'euw')