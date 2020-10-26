import socket

from inspectors.misc import MiscChallengeInspector


class MazeInspector(MiscChallengeInspector):
    def solve(self) -> bool:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.host, self.port))

            for _ in range(5):
                data = s.recv(4096).decode().split('\n')

                maze = data[4:-2]
                height = len(maze)
                width = len(maze[0])
                seen = [[False] * width for _ in range(height)]
                stack = [(1, 1, '')]

                ans = self.__dfs(height, maze, seen, stack, width)
                s.sendall(ans.encode())

            final_res = s.recv(8192).decode()
            assert self.flag in final_res

            self.logger.info(self.msg_succeeded_to_solve())
            return True

        except:
            self.logger.warning(self.msg_failed_to_solve())
            return False

        finally:
            s.close()

    @staticmethod
    def __dfs(height, maze, seen, stack, width) -> str:
        try:
            s = ''
            while stack:
                h, w, way = stack.pop()
                if maze[h][w] == 'G':
                    s = way
                    break

                seen[h][w] = True
                for nh, nw, ns in [(h - 1, w, 'U'), (h, w + 1, 'R'), (h + 1, w, 'D'), (h, w - 1, 'L')]:
                    if 0 < nh < height and 0 < nw < width and (maze[nh][nw] == ' ' or maze[nh][nw] == 'G') and not \
                            seen[nh][nw]:
                        stack.append((nh, nw, ''.join([way, ns])))
            return s
        except:
            raise
