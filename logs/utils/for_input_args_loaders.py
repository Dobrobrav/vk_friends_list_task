from .common import logger


def log_start_loading_terminal_args():
    logger.info(f"Start loading args from terminal")


def log_finish_loading_terminal_args():
    logger.info(f"Successfully loaded args from terminal")


def log_start_validating_terminal_args():
    logger.info(f"Start validating args from terminal")


def log_finish_validating_terminal_args():
    logger.info(f"Successfully validated args from terminal")
