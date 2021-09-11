import requests
import os
from pathlib import Path

import settings


class FileHandler:
    @classmethod
    async def get_media(cls, status):
        if hasattr(status, "retweeted_status"):
            return

        if 'media' not in status.entities:
            return

        url = None
        id = status.user.id
        user_name = status.user.name
        print('START FIND MEDIA')
        for media in status.extended_entities['media']:
            if "video_info" not in media:
                print('PHOTO FILE')
                url = media["media_url_https"]
                cls.get_file(id, user_name, url)
                continue

            bitrate = 0
            video_info = media["video_info"]
            for vid in video_info["variants"]:
                print('VIDEO FILE')
                if "bitrate" not in vid:
                    continue

                if bitrate <= vid["bitrate"]:
                    bitrate = vid["bitrate"]
                    url = vid["url"]

            cls.get_file(id, user_name, url)
        print('END FIND MEDIA')

    @classmethod
    def get_file(cls, user_id, user_name, url):
        path = f'{settings.BASE_PATH}{user_id}/'
        Path(path).mkdir(parents=True, exist_ok=True)

        print(f'Start Folder Write: {path}')
        try:
            print(f'START USERNAME TEXT, USERNAME: {user_name}')
            if not os.path.exists(path + user_name):
                with open(path + user_name, 'w'): pass
            print(f'END USERNAME TEXT, USERNAME: {user_name}')
        except:
            print(f'ERROR USERNAME TEXT, USERNAME: {user_name}')
            pass

        media_url = requests.get(url)
        file_name = url.split('/')[-1].split('?')[0]
        file_path = path + file_name
        print(f'START WRITE MEDIA FILE, PATH: {file_path}')
        if not os.path.exists(file_path):
            open(file_path, 'wb').write(media_url.content)
        print(f'END WRITE MEDIA FILE, PATH: {file_path}')
