import csv
import json
import tsv
from abc import ABC, abstractmethod
from typing import Sequence, Literal

import common
from .common import FriendDataPretty


class ISaver(ABC):

    @abstractmethod
    def save(self,
             friends: Sequence[FriendDataPretty],
             ) -> None:
        pass


class LocalStorageSaverMixin:
    _output_path: str

    def __init__(self,
                 output_path: str,
                 ) -> None:
        self._output_path = output_path


class CSVSaver(ISaver, LocalStorageSaverMixin):

    def save(self,
             friends: Sequence[FriendDataPretty],
             ) -> None:
        log_start_saving(self._output_path, 'csv')

        with open(f'{self._output_path}.csv', mode='w',
                  encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, friends[0].keys())
            writer.writeheader()
            writer.writerows(friends)

        log_finish_saving(self._output_path, 'csv')


class TSVSaver(ISaver, LocalStorageSaverMixin):

    def save(self,
             friends: Sequence[FriendDataPretty],
             ) -> None:
        log_start_saving(self._output_path, 'tsv')

        with open(f'{self._output_path}.tsv', mode='w',
                  encoding='utf-8', newline='') as file:
            writer = tsv.TsvWriter(file)
            writer.line(*friends[0].keys())
            for friend in friends:
                writer.line(*friend.values())

        log_finish_saving(self._output_path, 'tsv')


class JSONSaver(ISaver, LocalStorageSaverMixin):

    def save(self,
             friends: Sequence[FriendDataPretty],
             ) -> None:
        log_start_saving(self._output_path, 'json')

        with open(f'{self._output_path}.json', mode='w',
                  encoding='utf-8', newline='') as file:
            json.dump(friends, fp=file, ensure_ascii=False)

        log_finish_saving(self._output_path, 'json')


def save_friends_data(friends: Sequence[FriendDataPretty],
                      output_path: str,
                      output_format: Literal['csv', 'tsv', 'json'],
                      ) -> None:
    match output_format:
        case 'csv':
            saver = CSVSaver(output_path)
        case 'tsv':
            saver = TSVSaver(output_path)
        case 'json':
            saver = JSONSaver(output_path)
        case _:
            raise ValueError('the format must be one of the allowed')

    saver.save(friends)


# LOGGING FUNCTIONS
def log_start_saving(output_path: str,
                     output_format: str,
                     ) -> None:
    common.logger.info(f"Start saving data to {output_format.upper()} "
                       f"{output_path}.{output_format} file")


def log_finish_saving(output_path: str,
                      output_format: str,
                      ) -> None:
    common.logger.info(f"Successfully saved data to {output_format.upper()} "
                       f"{output_path}.{output_format} file")
