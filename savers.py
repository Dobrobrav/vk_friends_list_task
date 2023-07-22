import csv
import json
import tsv
from abc import ABC, abstractmethod
from typing import Sequence
from common import FriendData


class ISaver(ABC):
    # in order not to brake the Liskov principal, possible to add __init__
    # instead of passing the differing arguments to the save func

    @abstractmethod
    def save(self,
             friends: Sequence[FriendData],
             out_path: str,
             ) -> None:
        pass


class CSVSaver(ISaver):

    def save(self,
             friends: Sequence[FriendData],
             out_path: str,
             ) -> None:
        with open(f'{out_path}.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, friends[0].keys())
            writer.writeheader()
            writer.writerows(friends)


class TSVSaver(ISaver):

    def save(self,
             friends: Sequence[FriendData],
             out_path: str,
             ) -> None:
        with open(f'{out_path}.tsv', 'w', encoding='utf-8', newline='') as file:
            writer = tsv.TsvWriter(file)
            writer.line(*friends[0].keys())
            for friend in friends:
                writer.line(*friend.values())


class JSONSaver(ISaver):

    def save(self,
             friends: Sequence[FriendData],
             out_path: str,
             ) -> None:
        with open(f'{out_path}.json', 'w', encoding='utf-8', newline='') as file:
            json.dump(friends, fp=file, ensure_ascii=False)
