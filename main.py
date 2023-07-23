from typing import Literal, Sequence
from common import FriendData
from data_loaders import VkDataLoader
from exceptions import IncorrectInput
from input_args_loaders import TerminalArgsLoader
from savers import CSVSaver, TSVSaver, JSONSaver


def main():
    try:
        args_in = TerminalArgsLoader().load()
        friends_data = VkDataLoader().load_friends_data(
            user_id=args_in.user_id,
            auth_token=args_in.auth_token,
            page=args_in.page,
            limit=args_in.limit,
        )
        save_friends_data(friends_data, args_in.out_path, args_in.out_format)
    except IncorrectInput as e:
        print(f"Please type {e.expected_value_descr}"
              f" for <{e.arg_name}> argument")
    except Exception as e:
        print(f'Something unexpected went wrong. Error message: {e}. '
              f'Please check the input arguments and try again (maybe later)')
        # log it
    else:
        print('Successful!')


def save_friends_data(friends: Sequence[FriendData],
                      out_path: str,
                      out_format: Literal['csv', 'tsv', 'json'],
                      ) -> None:
    match out_format:
        case 'csv':
            saver = CSVSaver(out_path)
        case 'tsv':
            saver = TSVSaver(out_path)
        case 'json':
            saver = JSONSaver(out_path)
        case _:
            raise ValueError('the format must be one of the allowed')

    saver.save(friends)


if __name__ == '__main__':
    main()
