import logging
import re
import sys
from typing import IO
import urllib.error
import urllib.parse

import asyncio
from api_request import setup, main

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)

if __name__ == "__main__":
    dbc, start, rtyp, default_sleep_time, total = setup()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(dbc, start, rtyp, default_sleep_time, total))
