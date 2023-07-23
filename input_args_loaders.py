import argparse
import sys
from abc import ABC, abstractmethod
from typing import NamedTuple, Literal

import common
from exceptions import IncorrectInput


class InputArgs(NamedTuple):
    auth_token: str
    user_id: int
    out_format: Literal['csv', 'tsv', 'json']
    out_path: str
    page: int | None
    limit: int | None


class IInputArgsLoader(ABC):
    _ALLOWED_OUT_FORMATS = ('csv', 'tsv', 'json')

    @abstractmethod
    def load(self):
        pass


class TerminalArgsLoader(IInputArgsLoader):

    def load(self) -> InputArgs:
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

        return self._filter_input_args(parser.parse_args())

    def _filter_input_args(self,
                           args_in: argparse.Namespace,
                           ) -> InputArgs:
        self._validate_args_in(args_in)

        return InputArgs(
            auth_token=args_in.auth_token,
            user_id=args_in.user_id,
            out_path=args_in.out_path,
            out_format=args_in.out_format.lower(),
            page=args_in.page,
            limit=args_in.limit,
        )

    @staticmethod
    def _validate_args_in(args_in: argparse.Namespace,
                          ) -> None:
        try:
            common.validate_positive_int_or_none(args_in.page)
        except (TypeError, ValueError):
            raise IncorrectInput(
                arg_name='page',
                expected_value_descr='a positive integer',
            )
        try:
            common.validate_positive_int_or_none(args_in.limit)
        except (TypeError, ValueError):
            raise IncorrectInput(
                arg_name='limit',
                expected_value_descr='a positive integer',
            )
