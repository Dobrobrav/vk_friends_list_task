import argparse
from abc import ABC, abstractmethod
import common


class IInputArgsLoader(ABC):
    """ Loads input arguments """
    _ALLOWED_OUT_FORMATS = ('csv', 'tsv', 'json')

    @abstractmethod
    def load(self):
        pass


class TerminalArgsLoader(IInputArgsLoader):
    """ Loads input arguments from terminal """

    def load(self) -> common.InputArgs:
        log_start_loading_terminal_args()

        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-a', '--auth_token', type=str,
            help='Auth token for vk', required=True,
        )
        parser.add_argument(
            '-uid', '--user_id', type=int,
            help='Vk user id', required=True,
        )
        parser.add_argument(
            '-f', '--out_format', type=str, help='Output file format',
            default='csv', choices=self._ALLOWED_OUT_FORMATS,
        )
        parser.add_argument(
            '-p', '--out_path', type=str,
            help='Output file path', default='report',
        )
        parser.add_argument(
            '-pg', '--page', type=int, help='Number of page'
        )
        parser.add_argument(
            '-lim', '--limit', type=int,
            help='Quantity of rows in a single page (positive)'
        )
        args = parser.parse_args()
        self._validate_input_args(args)
        filtered_args = self._filter_input_args(args)

        log_finish_loading_terminal_args()

        return filtered_args

    def _filter_input_args(self,
                           input_args: argparse.Namespace,
                           ) -> common.InputArgs:
        return common.InputArgs(
            auth_token=input_args.auth_token,
            user_id=input_args.user_id,
            output_path=input_args.out_path,
            output_format=input_args.out_format.lower(),
            page=input_args.page,
            limit=input_args.limit,
        )

    @staticmethod
    def _validate_input_args(input_args: argparse.Namespace,
                             ) -> None:
        log_start_validating_terminal_args()

        try:
            common.validate_positive_int_or_none(input_args.page)
        except (TypeError, ValueError):
            raise common.InvalidInputError(
                arg_name='page',
                expected_value_descr='a positive integer',
                log_error_descr='Invalid page value',
            )
        try:
            common.validate_positive_int_or_none(input_args.limit)
        except (TypeError, ValueError):
            raise common.InvalidInputError(
                arg_name='limit',
                expected_value_descr='a positive integer',
                log_error_descr='Invalid limit value',
            )

        log_finish_validating_terminal_args()


# LOGGING FUNCTIONS
def log_start_loading_terminal_args():
    common.logger.info(f"Start loading args from terminal")


def log_finish_loading_terminal_args():
    common.logger.info(f"Successfully loaded args from terminal")


def log_start_validating_terminal_args():
    common.logger.info(f"Start validating args from terminal")


def log_finish_validating_terminal_args():
    common.logger.info(f"Successfully validated args from terminal")
