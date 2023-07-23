from loguru import logger

# remove default loguru handler to stop logging to terminal
logger.remove()
# set up logger to log to file
logger.add("logs/app_log.log", rotation="1 day", level='INFO')


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
