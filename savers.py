import csv
import json
import os

import tsv
from abc import ABC, abstractmethod
from typing import Sequence, Literal
import common
import log_utils


class ISaver(ABC):

    @abstractmethod
    def save(self,
             friends: Sequence[common.FriendDataPretty],
             ) -> None:
        pass


class LocalStorageSaverMixin:
    _output_path: str

    def __init__(self,
                 output_path: str,
                 ) -> None:
        self._output_path = output_path

    def _allow_create_dirs_if_necessary(self,
                                        path: str,
                                        ) -> None:
        if '/' in self._output_path:
            self._allow_create_dirs(path)

    @staticmethod
    def _allow_create_dirs(path: str,
                           ) -> None:
        # Extract the directory path from the 'path' variable
        parent_directory = os.path.dirname(path)
        # Ensure the parent directory for the file exists
        os.makedirs(parent_directory, exist_ok=True)


class CSVSaver(ISaver, LocalStorageSaverMixin):
    """ Saves to '.csv' format """

    def save(self,
             friends: Sequence[common.FriendDataPretty],
             ) -> None:
        log_utils.log_start_saving(self._output_path, 'csv')

        self._allow_create_dirs_if_necessary(self._output_path)

        with open(f'{self._output_path}.csv', mode='w',
                  encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, friends[0].keys())
            writer.writeheader()
            writer.writerows(friends)

        log_utils.log_finish_saving(self._output_path, 'csv')


class TSVSaver(ISaver, LocalStorageSaverMixin):
    """ Saves to '.tsv' format """

    def save(self,
             friends: Sequence[common.FriendDataPretty],
             ) -> None:
        log_utils.log_start_saving(self._output_path, 'tsv')

        self._allow_create_dirs_if_necessary(self._output_path)

        with open(f'{self._output_path}.tsv', mode='w',
                  encoding='utf-8', newline='') as file:
            writer = tsv.TsvWriter(file)
            writer.line(*friends[0].keys())
            for friend in friends:
                writer.line(*friend.values())

        log_utils.log_finish_saving(self._output_path, 'tsv')


class JSONSaver(ISaver, LocalStorageSaverMixin):
    """ Saves to '.json' format """

    def save(self,
             friends: Sequence[common.FriendDataPretty],
             ) -> None:
        log_utils.log_start_saving(self._output_path, 'json')

        self._allow_create_dirs_if_necessary(self._output_path)

        with open(f'{self._output_path}.json', mode='w',
                  encoding='utf-8', newline='') as file:
            json.dump(friends, fp=file, ensure_ascii=False)

        log_utils.log_finish_saving(self._output_path, 'json')


def save_friends_data(friends_data: Sequence[common.FriendDataPretty],
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

    saver.save(friends_data)
