import sys
from typing import TypeAlias, Literal, NamedTuple
from pydantic import BaseModel

FriendDataPretty: TypeAlias = dict[str, str | int]  # russian titles and other


class InputArgs(NamedTuple):
    auth_token: str
    user_id: int | None
    output_path: str
    output_format: Literal['csv', 'tsv', 'json']
    page: int | None
    limit: int | None


# ERRORS
class InvalidInputError(Exception):
    arg_name: str
    expected_value_descr: str
    log_error_descr: str

    def __init__(self,
                 arg_name: str,
                 expected_value_descr: str,
                 log_error_descr: str,
                 ) -> None:
        self.arg_name = arg_name
        self.expected_value_descr = expected_value_descr
        self.log_error_descr = log_error_descr


class ClosedVkProfileError(Exception):
    pass


class UnexpectedVkError(Exception):
    pass


# PYDANTIC CLASSES
class ResponseWrapper(BaseModel):
    response: 'Response'


class Response(BaseModel):
    count: int
    items: list['FriendData']


class FriendData(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    country: 'Country | None' = None
    city: 'City | None' = None
    bdate: str | None = None
    sex: Literal[1, 2] | None = None


class City(BaseModel):
    id: int
    title: str


class Country(BaseModel):
    id: int
    title: str


# FUNCTIONS
def is_any_argv_typed():
    """ Checks if any arguments were added after "python main.py" in terminal """
    if len(sys.argv) == 1:
        return False
    return True


def validate_positive_int_or_none(value: int | None,
                                  ) -> None:
    is_not_none_nor_int = value is not None and type(value) is not int
    if is_not_none_nor_int:
        raise TypeError()
    is_non_positive_int = type(value) is int and value <= 0
    if is_non_positive_int:
        raise ValueError()
