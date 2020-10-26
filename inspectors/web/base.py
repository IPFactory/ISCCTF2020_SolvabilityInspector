from abc import ABCMeta

import requests

from inspectors import ChallengeInspector


class WebChallengeInspector(ChallengeInspector, metaclass=ABCMeta):
    def __init__(self, name: str, host: str, port: str, flag: str):
        super().__init__(name, host, port, flag, category='Web')
        self.url = f'http://{host}:{port}/' if port else f'http://{host}/'

    def connect(self):
        try:
            assert requests.get(self.url).status_code == 200
            self.logger.info(self.msg_succeeded_to_connect())
            return True
        except:
            self.logger.warning(self.msg_failed_to_connect())
            return False
