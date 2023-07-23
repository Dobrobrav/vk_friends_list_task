from typing import Literal, Sequence

import pydantic_core

from common import FriendDataPretty
from data_loaders import VkDataLoader
from exceptions import InvalidInput, UnknownVkError
from input_args_loaders import ArgsFromTerminalLoader
from savers import CSVSaver, TSVSaver, JSONSaver


def main():
    try:
        input_args = ArgsFromTerminalLoader().load()
        friends_data = VkDataLoader().load_friends_data(
            user_id=input_args.user_id,
            auth_token=input_args.auth_token,
            page=input_args.page,
            limit=input_args.limit,
        )
        save_friends_data(friends_data,
                          input_args.output_path,
                          input_args.output_format)
    except InvalidInput as e:
        print(f"Please type {e.expected_value_descr}"
              f" for <{e.arg_name}> argument and try again")
    except pydantic_core.ValidationError:
        print(f"Something went wrong with vk response. "
              f"Please try again later.")
    except UnknownVkError:
        print('Something went wrong with the request to vk.'
              'Please check the arguments you typed and try again (maybe later')
    except Exception as e:
        print(f'Something unexpected went wrong. Error message: {e}. '
              f'Please check the input arguments and try again (maybe later)')
    # log it
    else:
        print('Successful!')


def save_friends_data(friends: Sequence[FriendDataPretty],
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
