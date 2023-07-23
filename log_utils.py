import json

from loguru import logger
import datetime

from common import FriendDataPretty

# remove default loguru handler to stop logging to terminal
logger.remove()
# set up logger to log to file
today_date = datetime.date.today()
logger.add(f"logs/app_log.{today_date}.log", rotation="1 day", level='INFO')


def log_start_loading_friends_data(user_id: int,
                                   ) -> None:
    logger.info(f"Start loading friends data for {user_id}")


def log_finish_loading_friends_data(user_id: int,
                                    friends_data_pretty: list[FriendDataPretty],
                                    ) -> None:
    # logger.info(f"Finish loading friends data for {user_id}, "
    #             f"data: {json.dumps(friends_data_pretty, ensure_ascii=False)}")
    logger.info(f"Finish loading friends data for {user_id}")


def log_start_validating_response():
    logger.info(f"Start validating vk response")


def log_finish_validating_response():
    logger.info(f"Finish validating vk response")


def log_start_http_request(url: str,
                           ) -> None:
    logger.info(f"Start HTTP-request to {url}")


def log_finish_http_request(url: str,
                            ) -> None:
    logger.info(f"Finish HTTP-request to {url}")


def log_start_saving(output_path: str,
                     output_format: str,
                     ) -> None:
    logger.info(f"Start saving data to {output_format.upper()} "
                f"{output_path}.{output_format} file")


def log_finish_saving(output_path: str,
                      output_format: str,
                      ) -> None:
    logger.info(f"Finish saving data to {output_format.upper()} "
                f"{output_path}.{output_format} file")
