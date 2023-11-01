import argparse
import logging
import psutil
import time
from datetime import datetime

import requests

LOGFILE_NAME = 'memory_script_logfile.log'
LOGFILE_ENCODING = 'utf-8'
DEFAULT_MEMORY_ALARM_THRESHOLD = 90.0  # percentage
CHECKING_INTERVAL = 300  # in seconds
TOLERATED_AMOUNT_OF_ERRORS = 10


class BadResponseException(Exception):
    """For bad (non-200 status code) response from server."""
    pass


def get_args() -> tuple[str, float]:
    """Process args. If address is not provided - raises AssertionError."""
    args = parser.parse_args()
    assert isinstance(args.address, str)
    return args.address, args.mem_target


def check_memory(target: float) -> bool:
    """Returns False if memory consumtion is over its threshold."""
    mem = psutil.virtual_memory()
    if mem.percent > target:
        return False
    return True


def send_alarm(address: str) -> None:
    """
    Assuming single GET request on provided address will be enough for
    alarm this part is minimized.
    """
    response = requests.get(address)
    if response.status_code != 200:
        raise BadResponseException("Server didn't return 200.")


def main(address: str, target_memory: float):
    """
    Performs an infinite loop cycle until it is manually stopped or when the
    count of errors exceeds the threshold.
    """
    while True:
        counter = 0
        try:
            if not check_memory(target_memory):
                send_alarm(address)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logging.error(f'An unexpected error has occured {datetime.now()}, '
                          f'printing it below.\n\n{e}')
            counter += 1
            if counter > TOLERATED_AMOUNT_OF_ERRORS:
                raise
        time.sleep(CHECKING_INTERVAL)


if __name__ == '__main__':
    logging.basicConfig(
        filename=LOGFILE_NAME,
        encoding=LOGFILE_ENCODING,
        level=logging.ERROR
    )
    parser = argparse.ArgumentParser(
        description=('If memory consumption exceeds target threshold - send '
                     'alarm to API server')
    )
    parser.add_argument('address', nargs='?', default=None,
                        help='API server address')
    parser.add_argument('mem_target', nargs='?',
                        default=DEFAULT_MEMORY_ALARM_THRESHOLD, type=float,
                        help='Memory target threshold')
    address, target_memory = get_args()
    main(address, target_memory)
