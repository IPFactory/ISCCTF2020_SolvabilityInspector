import abc
import logging
import os
import sys
import typing
from typing import Union

import requests

BASIC_LOG_FORMAT = f'[%(levelname)s] %(name)s(%(asctime)s) : %(message)s'
logging.basicConfig(level=logging.INFO, format=BASIC_LOG_FORMAT, stream=sys.stdout)


class ChallengeInspector(object, metaclass=abc.ABCMeta):
    def __init__(self, name: str, host: str, port: Union[int, str], flag: str, category: str) -> None:
        self.category = category
        self.name = name
        self.host = host
        self.port = int(port)
        self.flag = flag
        self.is_alive = True

        # logger config
        self.logger = logging.getLogger(self.__class__.__name__)

        logging_err_handler = logging.StreamHandler(sys.stderr)
        logging_err_handler.setLevel(logging.WARN)
        logging_err_handler.setFormatter(logging.Formatter(f'\x1b[31m{BASIC_LOG_FORMAT}\x1b[0m'))
        self.logger.addHandler(logging_err_handler)

    def check_alive(self) -> bool:
        CONNECTABLE = self.connect()
        SOLVABLE = self.solve() if CONNECTABLE else False  # 繋がらなければ解けない
        IS_ALIVE = all([CONNECTABLE, SOLVABLE])

        if IS_ALIVE:
            self.logger.info(self.msg_is_alive())
            self.__notify_to_discord(f':white_check_mark: {self.msg_is_alive()}')
        else:
            self.logger.warning(self.msg_is_dead())
            msg = f':warning: {self.msg_is_dead()} ' \
                  f'[connectable?: {[":x:", ":o:"][CONNECTABLE]}] ' \
                  f'[solvable?: {[":x:", ":o:"][SOLVABLE]}] '
            self.__notify_to_discord(
                msg,
                who_to_notify=int(os.getenv('DISCORD_ORGANIZER_ROLE_ID') or '0')
            )

        self.is_alive = IS_ALIVE
        return IS_ALIVE

    @abc.abstractmethod
    def connect(self) -> bool:
        pass

    @abc.abstractmethod
    def solve(self) -> bool:
        pass

    def msg_is_alive(self) -> str:
        return f'[{self.category}]`{self.name}` is alive'

    def msg_is_dead(self) -> str:
        return f'[{self.category}]`{self.name}` is dead'

    def msg_succeeded_to_connect(self) -> str:
        return f'Succeeded to connect [{self.category}]{self.name}'

    def msg_failed_to_connect(self) -> str:
        return f'Failed to connect [{self.category}]{self.name}'

    def msg_succeeded_to_solve(self) -> str:
        return f'Succeeded to solve [{self.category}]{self.name}'

    def msg_failed_to_solve(self) -> str:
        return f'Failed to solve [{self.category}]{self.name}'

    @staticmethod
    def __notify_to_discord(msg: str, *, who_to_notify: int = None):
        if webhook_url := os.getenv('DISCORD_WEBHOOK_URL'):
            msg = f'{msg} <@&{who_to_notify}>' if who_to_notify else msg
            requests.post(webhook_url, data={'content': msg})


def execute_mul_inspect(inspetors: typing.List[ChallengeInspector]):
    for one in inspetors:
        one.check_alive()
