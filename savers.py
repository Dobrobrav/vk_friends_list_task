import csv
import json
import tsv
from abc import ABC, abstractmethod
from typing import Sequence
from common import FriendData


class ISaver(ABC):

    @abstractmethod
    def save(self,
             friends: Sequence[FriendData],
             ) -> None:
        pass


class StorageSaverMixin:
    _out_path: str

    def __init__(self,
                 out_path: str,
                 ) -> None:
        self._out_path = out_path


class CSVSaver(ISaver, StorageSaverMixin):

    def save(self,
             friends: Sequence[FriendData],
             ) -> None:
        with open(f'{self._out_path}.csv', mode='w',
                  encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, friends[0].keys())
            writer.writeheader()
            writer.writerows(friends)


class TSVSaver(ISaver, StorageSaverMixin):

    def save(self,
             friends: Sequence[FriendData],
             ) -> None:
        with open(f'{self._out_path}.tsv', mode='w',
                  encoding='utf-8', newline='') as file:
            writer = tsv.TsvWriter(file)
            writer.line(*friends[0].keys())
            for friend in friends:
                writer.line(*friend.values())


class JSONSaver(ISaver, StorageSaverMixin):

    def save(self,
             friends: Sequence[FriendData],
             ) -> None:
        with open(f'{self._out_path}.json', mode='w',
                encoding='utf-8', newline='') as file:
            json.dump(friends, fp=file, ensure_ascii=False)
