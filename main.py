#!/usr/bin/env python

import asyncio
from core.cli import Cli
from core.check_dependencies import check as dependency_check


async def main():
    if dependency_check():
        cli = Cli()
        await cli.run()


if __name__ == "__main__":
    asyncio.run(main())
