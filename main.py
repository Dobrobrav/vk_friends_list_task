from typing import Literal, Sequence
from common import FriendRow
from data_loaders import VkDataLoader
from input_args_loaders import TerminalArgumentsLoader
from savers import CSVSaver, TSVSaver, JSONSaver


def main():
    args_in = TerminalArgumentsLoader().load()
    friends_data = VkDataLoader().load_friends_data(
        args_in.user_id, args_in.auth_token
    )
    save_friends_data(friends_data, args_in.out_path, args_in.out_format)


def save_friends_data(friends: Sequence[FriendRow],
                      out_path: str,
                      out_format: Literal['csv', 'tsv', 'json'],
                      ) -> None:
    match out_format:
        case 'csv':
            saver = CSVSaver()
        case 'tsv':
            saver = TSVSaver()
        case 'json':
            saver = JSONSaver()
        case _:
            raise ValueError('the format must be one of the allowed')

    saver.save(friends, out_path)


if __name__ == '__main__':
    main()
