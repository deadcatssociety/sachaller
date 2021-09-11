import asyncio
import os
import time

import tweepy

import settings
from auth import Auth
from file_handler import FileHandler


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)
        except StopIteration:
            break


def main():
    api = Auth.get_api()
    while True:
        print('start')
        is_first = True
        for status in limit_handled(
                tweepy.Cursor(
                    api.list_timeline, list_id=settings.FAVORITE_LIST_ID, since_id=os.getenv('LAST_LIST_ID'),
                    count=settings.TWEET_COUNT, include_rts=False
                ).items()
        ):
            if is_first:
                is_first = False
                os.environ['LAST_LIST_ID'] = str(status.id)
            if 'media' not in status.entities:
                continue
            print('start file download')
            loop = asyncio.get_event_loop()
            loop.run_until_complete(FileHandler.get_media(status))
            print('end file download')
        print('wating')
        time.sleep(1 * 60)


if __name__ == "__main__":
    main()
