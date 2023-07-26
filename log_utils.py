import datetime
import pydantic_core
import requests

import common
import urllib3.exceptions
from loguru import logger

# remove default loguru handler to stop logs to terminal
logger.remove()

# set up logger to logs to file
today_date = datetime.date.today()
logger.add(f"logs/{today_date}.log", rotation="1 day", level='DEBUG')


# main.py FUNCTIONS:
def log_started() -> None:
    logger.info('Program started')


def log_finished() -> None:
    logger.info("Program finished successfully")


def log_invalid_input_error(e: common.InvalidInputError,
                            ) -> None:
    logger.error(e.log_error_descr)


def log_pydantic_validation_error(e: pydantic_core.ValidationError,
                                  ) -> None:
    logger.error(str(e))


def log_closed_vk_profile_error(e: common.ClosedVkProfileError,
                                ) -> None:
    logger.error(str(e))


def log_unexpected_vk_error(e: common.UnexpectedVkError,
                            ) -> None:
    logger.error(f"Unexpected vk error: {e}")


def log_bad_internet_connection(e: requests.exceptions.ConnectionError,
                                ) -> None:
    logger.error(f"Bad internet connection: {e}")


def log_unexpected_error(e: Exception,
                         ) -> None:
    logger.error(f"Unexpected error: {e}")


# input_args_loaders.py FUNCTIONS:
def log_start_loading_terminal_args():
    logger.info(f"Start loading args from terminal")


def log_finish_loading_terminal_args():
    logger.info(f"Successfully loaded args from terminal")


def log_start_validating_terminal_args():
    logger.info(f"Start validating args from terminal")


def log_finish_validating_terminal_args():
    logger.info(f"Successfully validated args from terminal")


# data_loaders.py FUNCTIONS:
def log_start_loading_friends_data(user_id: int,
                                   ) -> None:
    logger.info(f"Start loading friends data for {user_id}")


def log_finish_loading_friends_data(user_id: int,
                                    ) -> None:
    logger.info(f"Successfully finished loading friends data for {user_id}")


def log_start_validating_response():
    logger.info(f"Start validating vk response")


def log_finish_validating_response():
    logger.info(f"Successfully validated vk response")


def log_start_http_request(url: str,
                           ) -> None:
    logger.info(f"Start HTTP-request to {url}")


def log_finish_http_request(url: str,
                            ) -> None:
    logger.info(f"Successfully got HTTP-response from {url}")


# savers.py FUNCTIONS:
def log_start_saving(output_path: str,
                     output_format: str,
                     ) -> None:
    logger.info(f"Start saving data to {output_format.upper()} "
                f"{output_path}.{output_format} file")


def log_finish_saving(output_path: str,
                      output_format: str,
                      ) -> None:
    logger.info(f"Successfully saved data to {output_format.upper()} "
                f"{output_path}.{output_format} file")
