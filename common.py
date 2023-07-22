from typing import TypeAlias

FriendData: TypeAlias = dict[str, str | int]


def validate_positive_int_or_none(value: int | None,
                                  variable_name: str,
                                  ) -> None:
    is_not_none_and_int = value is not None and type(value) is not int
    is_non_positive_int = type(value) is int and value <= 0
    if is_not_none_and_int or is_non_positive_int:
        print(f"Please type a positive integer for {variable_name} argument")
        exit()
