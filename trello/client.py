""" Now.sh Module """

import requests
from .cache import Cache

API_BASE_URL = 'https://api.trello.com/1/'
BOARDS_CACHE_TIME = 300  # five minutes


class Client():
    """ Trello API client """

    def __init__(self, logger, api_key=None, api_token=None, webapp_command=None, app_class=None, user_data_dir=None):
        """ Constructor """
        self.logger = logger
        self.api_key = api_key
        self.api_token = api_token
        self.webapp_command = webapp_command
        self.app_class = app_class
        self.user_data_dir = user_data_dir

    def set_api_key(self, api_key):
        """ Sets thes API Key"""
        if self.api_key != api_key:
            self.api_key = api_key
            Cache.purge()

    def set_api_token(self, api_token):
        """ Sets thes API Token"""
        if self.api_token != api_token:
            self.api_token = api_token
            Cache.purge()

    def set_webapp_command(self, webapp_command):
        """ Sets thes API Token"""
        if self.webapp_command != webapp_command:
            self.webapp_command = webapp_command
            Cache.purge()

    def set_app_class(self, app_class):
        """ Sets thes API Token"""
        if self.app_class != app_class:
            self.app_class = app_class
            Cache.purge()

    def set_user_data_dir(self, user_data_dir):
        """ Sets thes API Token"""
        if self.user_data_dir != user_data_dir:
            self.user_data_dir = user_data_dir
            Cache.purge()

    def get_boards(self, filter_query=None):
        """ Returns A list of Trello boards, optionally filtered by 'filter_query' parameter """
        result = []

        if Cache.get("boards"):
            response = Cache.get("boards")
            self.logger.info('Cache hit')
        else:
            params = {
                "key": self.api_key,
                "token": self.api_token,
                "filter": 'open'
            }
            req = requests.get('%s/member/me/boards' % API_BASE_URL,
                               params=params)
            response = req.json()
            if req.status_code != 200:
                self.logger.error('Trello API Error: %s' % response)
                raise TrelloApiException(req.status_code, "Trello API Error")

            self.logger.info('Success response: %s' % response)
            Cache.set("boards", response, BOARDS_CACHE_TIME)

        for board in response:

            if filter_query is not None and filter_query.lower(
            ) not in board['name'].lower():
                continue

            script = '%s --app=%s --class=%s --user-data-dir=%s' % (self.webapp_command, board['url'], self.app_class, self.user_data_dir ) if bool(self.webapp_command) else None

            result.append({
                'id': board['id'],
                'name': board['name'],
                'description': board['desc'],
                'url': board['url'],
                'script': script
            })

        return result


class TrelloApiException(Exception):
    """ Trello exception """

    def __init__(self, status_code=500, message=""):
        Exception.__init__()
        self.status = status_code
        self.message = message

    def get_status_code(self):
        """ Returns the Status Code """
        return self.status
