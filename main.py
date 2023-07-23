import pydantic_core
from data_loaders import VkDataLoader
from exceptions import InvalidInput, UnknownVkError
from input_args_loaders import TerminalArgsLoader
from savers import save_friends_data
from loguru import logger

# remove default loguru handler to stop logging to terminal
logger.remove()
# set up logger to log to file
logger.add("logs/app_log.log", rotation="1 day", level='INFO')


def main():
    logger.info('Program started')
    print("STARTED")
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
    except InvalidInput as e:
        print(f"Please type {e.expected_value_descr}"
              f" for <{e.arg_name}> argument and try again")
        logger.error(e.log_error_descr)
    except pydantic_core.ValidationError:
        print(f"Vk response data structure is incorrect. "
              f"Please try again later.")
        logger.error("Wrong vk response data structure")
    except UnknownVkError as e:
        print('Something went wrong with the request to vk.'
              'Please check the arguments you typed and try again (maybe later)')
        logger.error(f"Unexpected vk error: {e}")
    except Exception as e:
        print(f'Something unexpected went wrong. Error message: {e}. '
              f'Please check the input arguments and try again (maybe later)')
        logger.error(f"Unexpected error: {e}")
    else:
        print('SUCCESSFUL!')
        logger.info("Program finished successfully")


if __name__ == '__main__':
    main()
