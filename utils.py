"""General purpose functions"""
import json
import os
from datetime import date
from dateutil.relativedelta import relativedelta
from constants import constants


class Config:
    """
    Class with configuration info

    Attributes:
        max_retries (int): Maximum number of times to retry a functions in case of errors
        start_date (str): Start date to get from the API
        end_date (str): End date do get from the API
        filepath (str): Path to save the data
    """

    def __init__(self) -> None:
        project_folder = os.path.dirname(__file__)
        config = self.load_config(project_folder=project_folder)

        self.validate_config(config=config)

        self.max_retries = int(
            config.get("max_retries", constants.DEFAULT_MAX_RETRIES.value)
        )
        data_folder = config.get(
            "data_folder",
            os.path.join(project_folder, "data"),
        )

        self.start_date = date.fromisoformat(
            config.get("start_date", constants.DEFAULT_START_DATE.value)
        )

        self.end_date = date.fromisoformat(
            config.get("end_date", constants.DEFAULT_END_DATE.value)
        )

        if self.start_date > self.end_date:
            raise ValueError("start_date greater than end_date")

        filename = (
            f"from_{self.start_date.isoformat()}_to_{self.end_date.isoformat()}.json"
        )
        self.filepath = os.path.join(data_folder, filename)

    def load_config(self, project_folder: str) -> dict:
        """
        Read config file

        Args:
            project_folder (str): The script folder

        Returns:
            dict: config file json dict
        """
        with open(
            os.path.join(project_folder, constants.CONFIG_FILE.value),
            "r",
            encoding="utf-8",
        ) as fi:
            return json.load(fi)

    def validate_config(self, config):
        """Validates the config.json file object

        Args:
            config: config json loaded object
        """
        if not isinstance(config, dict):
            raise TypeError("config json must be a dict")

        valid_params = ["start_date", "end_date", "max_retries", "data_folder"]

        unexpected_params = [a for a in config.keys() if a not in valid_params]
        if len(unexpected_params) > 0:
            raise ValueError(
                f"invalid config parameters: {', '.join(unexpected_params)}"
            )


def retry(max_retries: int):
    """
    Decorator to handle retries in functions
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(
                        f"[Attempt {attempt}/{max_retries}] Error in function {func.__name__}:\n{e}"
                    )

                    if attempt == max_retries:
                        raise e

        return wrapper

    return decorator
