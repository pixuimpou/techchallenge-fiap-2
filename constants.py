from enum import Enum
from datetime import date


class constants(Enum):
    """Constants values"""

    DEFAULT_MAX_RETRIES = 3
    CONFIG_FILE = "config.json"
    INVESTING_BASE_URL = "https://br.investing.com/"
    DEFAULT_START_DATE = "2000-12-27"
    DEFAULT_END_DATE = "2024-01-30"

    RAW_FILE_ID = "1l5vTZCEBk22HNw5ttfXuo3Q9l7XW-led"
    TIMESERIES_FILE_ID = "1r9gUdTkhdfxjtilV8YXO6_R-6gbJE2FK"
