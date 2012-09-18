#!/usr/bin/env python

import sys
import time
import requests
import gntp.notifier

GENERAL_NOTIFICATION = 'General'
API_ERROR_NOTIFICATION = 'API Error'
FRIEND_ONLINE_NOTIFICATION = 'Friend Online'
FRIEND_OFFLINE_NOTIFICATION = 'Friend Offline'
INVALID_GAMERTAG_ERROR = 'Invaid Gamertag'

with open('xblgrowl.png', 'r') as image:
    DEFAULT_ICON = image.read()

with open('error.png', 'r') as image:
    ERROR_ICON = image.read()

growl = gntp.notifier.GrowlNotifier(
    applicationName='Xbox Live',
    applicationIcon=DEFAULT_ICON,
    notifications=[
        GENERAL_NOTIFICATION,
        API_ERROR_NOTIFICATION,
        FRIEND_ONLINE_NOTIFICATION,
        FRIEND_OFFLINE_NOTIFICATION
    ],
)

growl.register()

def main(gamertag=None):
    online_cache = {}

    while True:
        if not gamertag:
            gamertag = raw_input('Xbox Live Gamertag: ')

        growl.notify(
            noteType=GENERAL_NOTIFICATION,
            title='Connecting...',
            description=gamertag,
        )

        player = None

        while True:
            response = requests.get('https://xboxapi.com/friends/%s' % gamertag, verify=False)
            results = response.json or {}
            error = results.get('Error')

            if error:
                growl.notify(
                    noteType=API_ERROR_NOTIFICATION,
                    title='API Error',
                    description=error,
                    icon=ERROR_ICON,
                )

            if error == INVALID_GAMERTAG_ERROR:
                gamertag = None
                break

            if not player and results.get('Player'):
                player = results.get('Player')

                growl.notify(
                    noteType=GENERAL_NOTIFICATION,
                    title='Connected',
                    description=player['Gamertag'],
                    icon=requests.get(player['Avatar']['Gamertile']['Small']).content,
                )

            for friend in results.get('Friends', []):
                presence = friend['Presence']

                if friend['RichPresence']:
                    presence += ':\n%s' % friend['RichPresence']

                if not friend['IsOnline']:
                    if friend['GamerTag'] in online_cache:
                        del online_cache[friend['GamerTag']]

                        growl.notify(
                            noteType=FRIEND_OFFLINE_NOTIFICATION,
                            title='%s is Offline' % friend['GamerTag'],
                            description=presence,
                            icon=requests.get(friend['LargeGamerTileUrl']).content,
                        )
                else:
                    if friend['GamerTag'] not in online_cache:
                        online_cache[friend['GamerTag']] = friend

                        growl.notify(
                            noteType=FRIEND_ONLINE_NOTIFICATION,
                            title='%s is Online' % friend['GamerTag'],
                            description=presence,
                            icon=requests.get(friend['LargeGamerTileUrl']).content,
                        )

            time.sleep(60)

if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
