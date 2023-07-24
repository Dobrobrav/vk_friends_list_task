import pydantic_core

import logs.utils.main_log
import print_utils
from data_loaders import VkDataLoader
from exceptions import InvalidInputError, UnexpectedVkError
from input_args_loaders import TerminalArgsLoader
from savers import save_friends_data


def main():
    logs.utils.main_log.log_started()
    print_utils.print_started()

    try:
        input_args = TerminalArgsLoader().load()
        friends_data = VkDataLoader().load_friends_data(
            user_id=input_args.user_id,
            auth_token=input_args.auth_token,
            page=input_args.page,
            limit=input_args.limit,
        )
        save_friends_data(friends_data,
                          input_args.output_path,
                          input_args.output_format)
    except InvalidInputError as e:
        print_utils.print_invalid_input(e)
        logs.utils.main_log.log_invalid_input_error(e)
    except pydantic_core.ValidationError as e:
        print_utils.print_pydantic_validation_error()
        logs.utils.main_log.log_pydantic_validation_error(e)

    except UnexpectedVkError as e:
        print_utils.print_unknown_vk_error()
        logs.utils.main_log.log_unexpected_vk_error(e)

    except Exception as e:
        print_utils.print_unexpected_error(e)
        logs.utils.main_log.log_unexpected_error(e)
    else:
        print_utils.print_finished()
        logs.utils.main_log.log_finished()


if __name__ == '__main__':
    main()
