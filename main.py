import pydantic_core
import common
import input_args_loaders
import savers
import data_loaders


def main():
    log_started()

    try:
        # if no args typed, use friendly interface
        if common.is_any_argv_typed():
            print_app_started_terminal_mode()
            input_args = input_args_loaders.TerminalArgsLoader().load()
        else:
            print_app_started_console_mode()
            input_args = input_args_loaders.ConsoleArgsLoader().load()

        friends_data = data_loaders.VkDataLoader().load_friends_data(
            user_id=input_args.user_id,
            access_token=input_args.auth_token,
            page=input_args.page,
            limit=input_args.limit,
        )
        savers.save_friends_data(
            friends_data=friends_data,
            output_path=input_args.output_path,
            output_format=input_args.output_format,
        )

    except common.InvalidInputError as e:
        print_invalid_input(e)
        log_invalid_input_error(e)
    except pydantic_core.ValidationError as e:
        print_pydantic_validation_error()
        log_pydantic_validation_error(e)
    except common.ClosedVkProfileError as e:
        print_closed_vk_profile_error()
        log_closed_vk_profile_error(e)
    except common.UnexpectedVkError as e:
        print_unknown_vk_error()
        log_unexpected_vk_error(e)
    except Exception as e:
        print_unexpected_error(e)
        log_unexpected_error(e)
    else:
        print_finished()
        log_finished()


# FRIENDLY PRINTING FUNCTIONS
def print_inter_arguments() -> None:
    print('Please type the required arguments: '
          '-a [AUTH_TOKEN], -uid [USER_ID]')


def print_app_started_terminal_mode() -> None:
    """ Prints that app has started if user provided argv arguments """
    print('Start working')


def print_app_started_console_mode() -> None:
    """ Print that app has started if user did not provide argv arguments """
    print("Welcome!")
    print("Here you can download list of your friends... (add description)")


def print_finished() -> None:
    print('Program finished successfully :)')


def print_invalid_input(e: common.InvalidInputError,
                        ) -> None:
    print(f"Please type {e.expected_value_descr}"
          f" for <{e.arg_name}> argument and try again")


def print_pydantic_validation_error() -> None:
    print(f"Vk response data structure is incorrect. "
          f"Please try again later.")


def print_closed_vk_profile_error() -> None:
    print(f"The profile is closed, so his friends' data can't be downloaded :(")


def print_unknown_vk_error() -> None:
    print('Something went wrong with the request to vk. '
          'Please check the arguments you typed and try again (maybe later)')


def print_unexpected_error(e: Exception,
                           ) -> None:
    print(f'Something unexpected went wrong. Error message: {e}. '
          f'Please check the input arguments and try again (maybe later)')


# LOGGING FUNCTIONS
def log_started() -> None:
    common.logger.info('Program started')


def log_finished() -> None:
    common.logger.info("Program finished successfully")


def log_invalid_input_error(e: common.InvalidInputError,
                            ) -> None:
    common.logger.error(e.log_error_descr)


def log_pydantic_validation_error(e: pydantic_core.ValidationError,
                                  ) -> None:
    common.logger.error(str(e))


def log_closed_vk_profile_error(e: common.ClosedVkProfileError,
                                ) -> None:
    common.logger.error(str(e))


def log_unexpected_vk_error(e: common.UnexpectedVkError,
                            ) -> None:
    common.logger.error(f"Unexpected vk error: {e}")


def log_unexpected_error(e: Exception,
                         ) -> None:
    common.logger.error(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()
