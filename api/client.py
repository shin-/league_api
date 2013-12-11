import os

import requests
import six

class APIError(requests.exceptions.HTTPError):
    def __init__(self, message, response):
        super(APIError, self).__init__(message, response=response)

    def __str__(self):
        message = super(APIError, self).__str__()

        if self.is_client_error():
            message = '{0} Client Error: {1}'.format(
                self.response.status_code, self.response.reason
            )

        elif self.is_server_error():
            message = '{0} Server Error: {1}'.format(
                self.response.status_code, self.response.reason
            )

        if self.response.content:
            message = '{0} ({1})'.format(message, self.response.content)

        return message

    def is_client_error(self):
        return 400 <= self.response.status_code < 500

    def is_server_error(self):
        return 500 <= self.response.status_code < 600


class RateLimitError(APIError):
    def __init__(self, message, response):
        super(RateLimitError, self).__init__(message, response=response)


class Client(requests.Session):
    def __init__(self, api_key):
        super(Client, self).__init__()
        self._api_key = api_key
        self._base = 'http://prod.api.pvp.net/api'

    def make_request(self, route, method, **kwargs):
        methods = {
            'get': self.get,
            'put': self.put,
            'delete': self.delete,
            'post': self.post
        }

        if 'params' in kwargs and kwargs['params']:
            kwargs['params']['api_key'] = self._api_key
        else:
            kwargs['params'] = {'api_key': self._api_key}

        response = methods[method.lower()](
            self._base + route,
            **kwargs
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise APIError(e, response)

        return response.json()

    def get_champions(self, free_to_play=False, region='na'):
        return self.make_request(
            '/lol/{0}/v1.1/champion'.format(region),
            'GET',
            params={'freeToPlay': free_to_play}
        )

    def get_recent_games(self, summoner_id, region='na'):
        return self.make_request(
            '/lol/{0}/v1.1/game/by-summoner/{1}/recent'.format(region, summoner_id),
            'GET'
        )

    def get_summoner_leagues(self, summoner_id, region='na'):
        return self.make_request(
            '/{0}/v2.1/league/by-summoner/{1}'.format(region, summoner_id),
            'GET'
        )

    def get_stats_summary(self, summoner_id, season=None, region='na'):
        if season:
            params = {'season': season}
        return self.make_request(
            '/lol/{0}/v1.1/stats/by-summoner/{1}/summary'.format(region, summoner_id),
            'GET',
            params=params
        )

    def get_ranked_stats(self, summoner_id, season=None, region='na'):
        if season:
            params = {'season': season}
        return self.make_request(
            '/lol/{0}/v1.1/stats/by-summoner/{1}/ranked'.format(region, summoner_id),
            'GET',
            params=params
        )

    def get_summoner_masteries(self, summoner_id, region='na'):
        return self.make_request(
            '/lol/{0}/v1.1/summoner/{1}/masteries'.format(region, summoner_id),
            'GET'
        )

    def get_summoner_runes(self, summoner_id, region='na'):
        return self.make_request(
            '/lol/{0}/v1.1/summoner/{1}/runes'.format(region, summoner_id),
            'GET'
        )

    def get_summoner_by_name(self, name, region='na'):
        return self.make_request(
            '/lol/{0}/v1.1/summoner/by-name/{1}'.format(region, name),
            'GET'
        )

    def get_summoner(self, summoner_id, region='na'):
        return self.make_request(
            '/lol/{0}/v1.1/summoner/{1}'.format(region, summoner_id),
            'GET'
        )

    def get_summoner_names(self, summoner_ids, region='na'):
        ids = ','.join(summoner_ids)
        return self.make_request(
            '/lol/{0}/v1.1/summoner/{1}/name'.format(region, ids),
            'GET'
        )

    def get_summoner_teams(self, summoner_id, region='na'):
        return self.make_request(
            '/{0}/v2.1/team/by-summoner/{1}'.format(region, summoner_id),
            'GET'
        )