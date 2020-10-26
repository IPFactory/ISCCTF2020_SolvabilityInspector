from inspectors.misc import MiscChallengeInspector


class ShellAintBadPlaceToBeInspector(MiscChallengeInspector):

    def solve(self) -> bool:
        self.logger.info(f'{self.msg_succeeded_to_solve()} (maybe)')
        return True
