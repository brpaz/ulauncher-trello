"""Ulauncher extension main  class"""

import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, PreferencesEvent, PreferencesUpdateEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem

from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from trello.client import Client as TrelloClient, TrelloApiException

LOGGER = logging.getLogger(__name__)


class TrelloExtension(Extension):
    """ Main extension class """

    def __init__(self):
        """ init method """
        super(TrelloExtension, self).__init__()
        LOGGER.info("Initializing Trello Extension")
        self.trello_client = TrelloClient(LOGGER)
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(PreferencesUpdateEvent,
                       PreferencesUpdateEventListener())


class KeywordQueryEventListener(EventListener):
    """ Handles Keyboard input """

    def on_event(self, event, extension):
        """ Handles the event """
        items = []

        try:
            boards = extension.trello_client.get_boards(
                event.get_argument())

            if not boards:
                return [ExtensionResultItem(
                    icon='images/icon.png',
                    name='No boards found with name %s' % event.get_argument(),
                    on_enter=HideWindowAction())
                ]

            for board in boards[:25]:
                items.append(ExtensionSmallResultItem(
                    icon='images/icon.png',
                    name=board['name'],
                    description=board['description'],
                    on_enter=OpenUrlAction(board['url']))
                )

        except TrelloApiException as e:  # pylint: disable=invalid-name
            LOGGER.error(e)
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Error when connecting to Trello API ( status code : %s )' % e.get_status_code(
                ),
                on_enter=HideWindowAction()))

        return RenderResultListAction(items)


class PreferencesEventListener(EventListener):
    """
    Listener for prefrences event.
    It is triggered on the extension start with the configured preferences
    """

    def on_event(self, event, extension):
        extension.trello_client.set_api_key(event.preferences['api_key'])
        extension.trello_client.set_api_token(event.preferences['api_token'])


class PreferencesUpdateEventListener(EventListener):
    """
    Listener for "Preferences Update" event.
    It is triggered when the user changes any setting in preferences window
    """

    def on_event(self, event, extension):
        if event.id == 'api_key':
            extension.trello_client.set_api_key(event.new_value)

        if event.id == 'api_token':
            extension.trello_client.set_api_token(event.new_value)


if __name__ == '__main__':
    TrelloExtension().run()
