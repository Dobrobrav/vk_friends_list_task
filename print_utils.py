import pydantic_core

from exceptions import InvalidInputError


# for main.py
def print_started():
    print("STARTED")


def print_finished():
    print('SUCCESSFUL!')


def print_invalid_input(e: InvalidInputError,
                        ) -> None:
    print(f"Please type {e.expected_value_descr}"
          f" for <{e.arg_name}> argument and try again")


def print_pydantic_validation_error() -> None:
    print(f"Vk response data structure is incorrect. "
          f"Please try again later.")


def print_unknown_vk_error() -> None:
    print('Something went wrong with the request to vk.'
          'Please check the arguments you typed and try again (maybe later)')


def print_unexpected_error(e: Exception,
                           ) -> None:
    print(f'Something unexpected went wrong. Error message: {e}. '
          f'Please check the input arguments and try again (maybe later)')
