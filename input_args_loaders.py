import argparse
import logging
from abc import ABC, abstractmethod
from typing import Optional, Literal, Collection, TypeVar

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

    def _filter_input_args(self,
                           input_args: argparse.Namespace,
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
            default_value='csv'
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
                         ) -> int | str | None:
        default_values_str = f' (default – {default_value})' if default_value else ''
        is_optional_str = f'(OPTIONAL) ' if is_empty_allowed else '(REQUIRED) '
        if allowed_values:
            allowed_values_str = f" (allowed – {', '.join(tuple(allowed_values))})"
        else:
            allowed_values_str = ''

        input_value = input(f"{is_optional_str}Please type {value_name}{default_values_str}{allowed_values_str}: ").strip()
        if is_empty_allowed and input_value.strip() == '':
            return default_value

        while True:
            try:
                if not is_empty_allowed and input_value == '':
                    raise ValueError()
                if input_type is not str:
                    self._validate_type(input_value, expected_type=input_type)
                if allowed_values:
                    self._validate_for_allowed_values(
                        input_value, allowed_values
                    )
                return input_value
            except (TypeError, ValueError):
                input_value = input(
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
                                     ) -> None:
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
