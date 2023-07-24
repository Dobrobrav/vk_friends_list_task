from loguru import logger
import datetime

# remove default loguru handler to stop logs to terminal
logger.remove()

# set up logger to logs to file
today_date = datetime.date.today()
logger.add(f"logs/log_files/{today_date}.log", rotation="1 day", level='DEBUG')
