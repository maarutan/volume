import sys
from argparse import ArgumentParser
from core.render import Render


class Cli:
    def __init__(self):
        self.render = Render()
        self.parser = ArgumentParser()
        self.parser.add_argument("--up", action="store_true", help="Increase volume")
        self.parser.add_argument("--down", action="store_true", help="Decrease volume")
        self.parser.add_argument(
            "--mute", action="store_true", help="Toggle volume mute"
        )
        self.parser.add_argument(
            "--micro", action="store_true", help="Toggle microphone mute"
        )

    async def run(self):
        args = self.parser.parse_args()

        if args.up:
            await self.render.add_volume("+")
        elif args.down:
            await self.render.add_volume("-")
        elif args.mute:
            self.render.toggle_volume()
        elif args.micro:
            self.render.toggle_micro()
        else:
            self.parser.print_help()
            sys.exit(1)
