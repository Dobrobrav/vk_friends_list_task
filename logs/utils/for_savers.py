from .common import logger


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
