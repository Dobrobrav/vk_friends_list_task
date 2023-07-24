from typing import TypeAlias

FriendDataPretty: TypeAlias = dict[str, str | int]


def validate_positive_int_or_none(value: int | None,
                                  ) -> None:
    is_not_none_nor_int = value is not None and type(value) is not int
    if is_not_none_nor_int:
        raise TypeError()
    is_non_positive_int = type(value) is int and value <= 0
    if is_non_positive_int:
        raise ValueError()

