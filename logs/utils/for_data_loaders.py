from utils.common import FriendDataPretty
from .common import logger


def log_start_loading_friends_data(user_id: int,
                                   ) -> None:
    logger.info(f"Start loading friends data for {user_id}")


def log_finish_loading_friends_data(user_id: int,
                                    friends_data_pretty: list[FriendDataPretty],
                                    ) -> None:
    # logger.info(f"Finish loading friends log_files for {user_id}, "
    #             f"log_files: {json.dumps(friends_data_pretty, ensure_ascii=False)}")
    logger.info(f"Successfully finished loading friends data for  {user_id}")


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
