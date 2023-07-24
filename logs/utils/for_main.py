import pydantic_core

from utils.exceptions import InvalidInputError, UnexpectedVkError
from .common import logger


def log_started():
    logger.info('Program started')


def log_finished():
    logger.info("Program finished successfully")


def log_invalid_input_error(e: InvalidInputError,
                            ) -> None:
    logger.error(e.log_error_descr)


def log_pydantic_validation_error(e: pydantic_core.ValidationError,
                                  ) -> None:
    logger.error(str(e))


def log_unexpected_vk_error(e: UnexpectedVkError,
                            ) -> None:
    logger.error(f"Unexpected vk error: {e}")


def log_unexpected_error(e: Exception,
                         ) -> None:
    logger.error(f"Unexpected error: {e}")
