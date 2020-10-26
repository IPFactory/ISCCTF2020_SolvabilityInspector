import re

import requests

from inspectors.web import WebChallengeInspector


class GreetinjsInspector(WebChallengeInspector):
    def solve(self) -> bool:
        BASE_URL = self.url

        # Step 1: Find a JS file used in the page.
        try:
            res = requests.get(BASE_URL + '/')
            m = re.search(r'(?<=<script src=").+?(?=" integrity)', res.text)
            js_path = m.group()  # expect: /js/greetjs
        except Exception:
            self.logger.warning(self.msg_failed_to_solve())
            return False

        # Step 2: Read the JS file.
        try:
            res = requests.get(BASE_URL + js_path)
            assert self.flag in res.text, self.logger.info(self.msg_succeeded_to_solve())

            self.logger.info(self.msg_succeeded_to_solve())
            return True
        except Exception:
            self.logger.warning(self.msg_failed_to_solve())
            return False
