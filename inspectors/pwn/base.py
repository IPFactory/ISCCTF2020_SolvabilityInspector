import socket
from abc import ABCMeta
from typing import Union

from inspectors import ChallengeInspector


class PwnChallengeInspector(ChallengeInspector, metaclass=ABCMeta):
    def __init__(self, name: str, host: str, port: Union[int, str], flag: str):
        super().__init__(name, host, port, flag, category='Pwn')

    def connect(self):
        s = socket.socket()
        s.settimeout(3)
        try:
            s.connect((self.host, self.port))
            self.logger.info(self.msg_succeeded_to_connect())
            return True
        except:
            self.logger.warning(self.msg_failed_to_connect())
            return False
        finally:
            s.close()
