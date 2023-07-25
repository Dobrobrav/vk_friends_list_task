import argparse
from abc import ABC, abstractmethod
from typing import Literal, Collection, TypeVar

import common

T = TypeVar('T')


class IInputArgsLoader(ABC):
    """ Loads input arguments """
    _ALLOWED_OUTPUT_FORMATS = ('csv', 'tsv', 'json')

    @abstractmethod
    def load(self):
        pass


class TerminalArgsLoader(IInputArgsLoader):
    """ Loads argv arguments from terminal after "python main.py" """

    def load(self) -> common.InputArgs:
        log_start_loading_terminal_args()

        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-a', '--auth_token', type=str,
            help='Auth token for vk', required=True,
        )
        parser.add_argument(
            '-uid', '--user_id', type=int, help='Vk user id',
        )
        parser.add_argument(
            '-p', '--output_path', type=str,
            help='Output file path', default='report',
        )
        parser.add_argument(
            '-f', '--output_format', type=str, help='Output file format',
            default='csv', choices=self._ALLOWED_OUTPUT_FORMATS,
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

    @staticmethod
    def _filter_input_args(input_args: argparse.Namespace,
                           ) -> common.InputArgs:
        return common.InputArgs(
            auth_token=input_args.auth_token,
            user_id=input_args.user_id,
            output_path=input_args.output_path,
            output_format=input_args.output_format.lower(),
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


class ConsoleArgsLoader(IInputArgsLoader):

    def load(self):
        input_args = common.InputArgs(
            auth_token=self._get_access_token(),
            user_id=self._get_user_id(),
            output_path=self._get_output_path(),
            output_format=self._get_output_format(),
            page=self._get_page(),
            limit=self._get_limit(),
        )
        return input_args

    def _get_access_token(self) -> str:
        input_value = self._ask_input_value(
            value_name='access token',
            is_empty_allowed=False,
        )
        return input_value

    def _get_user_id(self) -> int | None:
        input_value = self._ask_input_value(
            value_name='user id',
            input_type=int,
            is_empty_allowed=True,
        )
        return input_value

    def _get_output_path(self) -> str:
        input_value = self._ask_input_value(
            value_name='output path',
            is_empty_allowed=True,
            default_value='report',
        )
        return input_value

    def _get_output_format(self) -> Literal['csv', 'tsv', 'json']:
        input_value = self._ask_input_value(
            value_name='output format',
            is_empty_allowed=True,
            allowed_values=('csv', 'tsv', 'json'),
            default_value='csv',
            is_case_sensitive=False,
        )
        return input_value

    def _get_page(self) -> int | None:
        input_value = self._ask_input_value(
            value_name='page',
            input_type=int,
            is_empty_allowed=True,
        )
        return input_value

    def _get_limit(self) -> int | None:
        input_value = self._ask_input_value(
            value_name='max number of friends on a page',
            input_type=int,
            is_empty_allowed=True,
        )
        return input_value

    def _ask_input_value(self,
                         value_name: str,
                         is_empty_allowed: bool,
                         input_type: type[T] = str,
                         allowed_values: Collection[T] | None = None,
                         default_value: T | None = None,
                         is_case_sensitive: bool = True,
                         ) -> T | None:
        first_input_prompt = self._get_first_input_prompt(
            allowed_values, default_value, is_empty_allowed, value_name
        )

        first_input_value = input(first_input_prompt).strip()

        if is_empty_allowed and first_input_value.strip() == '':
            return default_value

        input_value = self.ask_repeat_value_if_necessary(
            is_empty_allowed, input_type, allowed_values,
            is_case_sensitive, value_name, first_input_value,
        )
        return input_value

    def _get_first_input_prompt(self,
                                allowed_values: Collection[T],
                                default_value: T,
                                is_empty_allowed: bool,
                                value_name: str,
                                ) -> str:
        default_value_str = self._get_default_value_str(default_value)
        is_optional_str = self._get_is_optional_str(is_empty_allowed)
        allowed_values_str = self._get_allowed_values_str(allowed_values)

        res = f"{is_optional_str}Please type " \
              f"{value_name}{default_value_str}{allowed_values_str}: "
        return res

    @staticmethod
    def _get_default_value_str(default_value: str | int,
                               ) -> str:
        return f' (default – {default_value})' if default_value else ''

    @staticmethod
    def _get_is_optional_str(is_empty_allowed: bool,
                             ) -> str:
        return f'(OPTIONAL) ' if is_empty_allowed else '(REQUIRED) '

    @staticmethod
    def _get_allowed_values_str(allowed_values: Collection[int | str],
                                ) -> str:
        if allowed_values:
            return f" (allowed – {', '.join(tuple(allowed_values))})"
        else:
            return ''

    def ask_repeat_value_if_necessary(self,
                                      is_empty_allowed: bool,
                                      input_type: type[T],
                                      allowed_values: Collection[T],
                                      is_case_sensitive: bool,
                                      value_name: str,
                                      first_input_value: str,
                                      ):
        while True:
            try:
                if not is_empty_allowed and first_input_value == '':
                    raise ValueError()
                if input_type is not str:
                    self._validate_type(first_input_value,
                                        expected_type=input_type)
                if allowed_values:
                    self._validate_for_allowed_values(
                        first_input_value, allowed_values, is_case_sensitive
                    )
                return first_input_value
            except (TypeError, ValueError):
                first_input_value = input(
                    f"Please, make sure, {value_name} "
                    f"is {input_type.__name__} and type it again: "
                )
                continue

    @staticmethod
    def _validate_type(value: str,
                       expected_type: type,
                       ) -> None:
        try:
            expected_type(value)
        except ValueError:
            raise TypeError()

    @staticmethod
    def _validate_for_allowed_values(input_value: T,
                                     allowed_values: Collection[T],
                                     case_sensitive: bool,
                                     ) -> None:
        if isinstance(input_value, str):
            input_value = input_value if case_sensitive else input_value.lower()

        if input_value not in allowed_values:
            raise ValueError()


# LOGGING FUNCTIONS
def log_start_loading_terminal_args():
    common.logger.info(f"Start loading args from terminal")


def log_finish_loading_terminal_args():
    common.logger.info(f"Successfully loaded args from terminal")


def log_start_validating_terminal_args():
    common.logger.info(f"Start validating args from terminal")


def log_finish_validating_terminal_args():
    common.logger.info(f"Successfully validated args from terminal")
