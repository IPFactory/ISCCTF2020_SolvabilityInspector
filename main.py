import os
import time

import dotenv
import schedule as schedule

from inspectors import execute_mul_inspect
from inspectors.misc import MazeInspector, ShellAintBadPlaceToBeInspector
from inspectors.pwn import EchoInspector, IterFoldInspector, PortalInspector, StuckInspector
from inspectors.web import CrackJwtInspector, GreetinjsInspector, MarkDamnItInspector, YonezerInspector

if __name__ == '__main__':
    dotenv.load_dotenv()

    pwn_stuck = StuckInspector(
        name=os.getenv('PWN_STUCK_NAME'),
        host=os.getenv('PWN_STUCK_HOST'),
        port=os.getenv('PWN_STUCK_PORT'),
        flag=os.getenv('PWN_STUCK_FLAG')
    )

    pwn_portal = PortalInspector(
        name=os.getenv('PWN_PORTAL_NAME'),
        host=os.getenv('PWN_PORTAL_HOST'),
        port=os.getenv('PWN_PORTAL_PORT'),
        flag=os.getenv('PWN_PORTAL_FLAG')
    )

    pwn_echo = EchoInspector(
        name=os.getenv('PWN_ECHO_NAME'),
        host=os.getenv('PWN_ECHO_HOST'),
        port=os.getenv('PWN_ECHO_PORT'),
        flag=os.getenv('PWN_ECHO_FLAG')
    )

    pwn_iter_fold = IterFoldInspector(
        name=os.getenv('PWN_ITER_FOLD_NAME'),
        host=os.getenv('PWN_ITER_FOLD_HOST'),
        port=os.getenv('PWN_ITER_FOLD_PORT'),
        flag=os.getenv('PWN_ITER_FOLD_FLAG')
    )

    misc_shell_aint_bad_place_to_be = ShellAintBadPlaceToBeInspector(
        name=os.getenv('MISC_SHELL_AINT_BAD_PLACE_TO_BE_NAME'),
        host=os.getenv('MISC_SHELL_AINT_BAD_PLACE_TO_BE_HOST'),
        port=os.getenv('MISC_SHELL_AINT_BAD_PLACE_TO_BE_PORT'),
        flag=os.getenv('MISC_SHELL_AINT_BAD_PLACE_TO_BE_FLAG')
    )

    misc_maze = MazeInspector(
        name=os.getenv('MISC_MAZE_NAME'),
        host=os.getenv('MISC_MAZE_HOST'),
        port=os.getenv('MISC_MAZE_PORT'),
        flag=os.getenv('MISC_MAZE_FLAG')
    )

    web_greetinjs = GreetinjsInspector(
        name=os.getenv('WEB_GREETINJS_NAME'),
        host=os.getenv('WEB_GREETINJS_HOST'),
        port=os.getenv('WEB_GREETINJS_PORT'),
        flag=os.getenv('WEB_GREETINJS_FLAG')
    )

    web_mark_damn_it = MarkDamnItInspector(
        name=os.getenv('WEB_MARK_DAMN_IT_NAME'),
        host=os.getenv('WEB_MARK_DAMN_IT_HOST'),
        port=os.getenv('WEB_MARK_DAMN_IT_PORT'),
        flag=os.getenv('WEB_MARK_DAMN_IT_FLAG'),
    )

    web_crackjwt = CrackJwtInspector(
        name=os.getenv('WEB_CRACKJWT_NAME'),
        host=os.getenv('WEB_CRACKJWT_HOST'),
        port=os.getenv('WEB_CRACKJWT_PORT'),
        flag=os.getenv('WEB_CRACKJWT_FLAG')
    )

    web_yonezer = YonezerInspector(
        name=os.getenv('WEB_YONEZER_NAME'),
        host=os.getenv('WEB_YONEZER_HOST'),
        port=os.getenv('WEB_YONEZER_PORT'),
        flag=os.getenv('WEB_YONEZER_FLAG')
    )

    chall_inspectors = [
        pwn_stuck,
        pwn_portal,
        pwn_echo,
        pwn_iter_fold,
        misc_shell_aint_bad_place_to_be,
        misc_maze,
        web_greetinjs,
        web_mark_damn_it,
        web_crackjwt,
        web_yonezer
    ]

    interval = int(os.getenv('INTERVAL'))
    schedule.every(interval).minutes.do(execute_mul_inspect, chall_inspectors)
    while True:
        schedule.run_pending()
        time.sleep(1)
