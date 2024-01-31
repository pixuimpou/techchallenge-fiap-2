import os
import json
from datetime import date, timedelta
from requests.exceptions import HTTPError
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from constants import constants
from utils import retry, Config

config = Config()


@retry(max_retries=config.max_retries)
def open_browser() -> WebDriver:
    """
    Opens the browser getting the investing site

    Returns:
        WebDriver: the browser object
    """
    options = Options()
    options.page_load_strategy = "eager"

    driver = webdriver.Chrome(options=options)
    driver.get(constants.INVESTING_BASE_URL.value + "indices/bovespa-historical-data")
    return driver


def make_api_url(base_url: str, **params) -> str:
    """
    Construct the complete api request url

    Args:
        base_url (str): API base url before query params
        **params: Query params to add to base url
    Returns:
        str: url in the format: base_url?param1=value2&param2=value2
    """
    base_url = base_url.rstrip("?/")
    params = [f"{p.strip()}={v.strip()}" for p, v in params.items()]
    return f"{base_url}?{'&'.join(params)}"


@retry(max_retries=config.max_retries)
def get_api_data(driver: WebDriver) -> dict:
    """
    Make the http request to get IBOVESPA data

    Args:
        driver (WebDriver): Browser driver
        start_date (date): Start date to get the data
        end_date (date): End date to get the data
    Returns:
        dict: API return json as dict
    """
    start_date = config.start_date
    step = 30
    end_date = start_date + timedelta(days=step)
    last_date = config.end_date
    full_data = []
    finished = False
    while not finished:
        params = {
            "start-date": start_date.isoformat(),
            "end-date": end_date.isoformat(),
            "time-frame": "Daily",
            "add-missing-rows": "false",
        }
        url = make_api_url(
            base_url="https://api.investing.com/api/financialdata/historical/17920",
            **params,
        )
        api_fetch_params = f"""
        {{
            'headers': {{
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'domain-id': 'br'
            }},
            'referrer': '{constants.INVESTING_BASE_URL.value}',
            'referrerPolicy': 'strict-origin-when-cross-origin',
            'body': null,
            'method': 'GET',
            'mode': 'cors',
            'credentials': 'omit'
        }}
        """
        api_fetch_callback = """
        response => {
                return response.text().then(data => ({ statusCode: response.status, data }));
        }
        """
        script = f"""
            var callback = arguments[arguments.length - 1];
            fetch('{url}', {api_fetch_params}).then({api_fetch_callback}).then(callback);
        """

        print(f"Making request to url {url}")
        response = driver.execute_async_script(script)
        status_code = response["statusCode"]
        data = response["data"]
        if status_code >= 300:
            raise HTTPError(
                f"request failed with status code : {status_code}\ndata: {data}"
            )
        data = json.loads(data)["data"]
        if isinstance(data, list):
            full_data += data
            print(f"Request succeded! Returned {len(data)} rows")
        elif data is None:
            print("Request returned empty!")
        if end_date == last_date:
            finished = True
        start_date = end_date + timedelta(days=1)
        end_date = end_date + timedelta(days=step + 1)
        end_date = min(end_date, last_date)
    return full_data


@retry(max_retries=config.max_retries)
def save_raw_data(data: dict):
    """
    Saves API returned json

    Args:
        data (str): data to write
    """
    path = config.filepath
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fi:
        print(f"Writing {len(data)} rows on path {path}")
        json.dump(data, fi)


def get_all_data():
    """Main function to orquestrate data extraction"""

    driver = open_browser()
    data = get_api_data(driver=driver)
    save_raw_data(data=data)
    driver.quit()


get_all_data()
