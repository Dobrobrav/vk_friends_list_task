import argparse
import csv
import json
import tsv

import requests
from typing import NamedTuple, Literal, Sequence, TypeAlias

FriendRow: TypeAlias = dict[str, str | int]


class InputArgs(NamedTuple):
    auth_token: str
    user_id: int
    out_format: Literal['csv', 'tsv', 'json']
    out_path: str


def main():
    args_in = get_input_args()
    friends_data = fetch_friends_data_rows(args_in.user_id, args_in.auth_token)

    save_friends_data_rows(friends_data, args_in.out_path, args_in.out_format)


def get_input_args() -> InputArgs:
    parser = argparse.ArgumentParser()
    arg_names = (
        'auth_token',
        'user_id',
        'out_format',
        'out_path',
    )
    for arg_name in arg_names:
        parser.add_argument(arg_name)

    args_in = parser.parse_args()
    args = InputArgs(
        auth_token=args_in.auth_token,
        user_id=args_in.user_id,
        out_path=args_in.out_path,
        out_format=args_in.out_format,
    )
    return args


def fetch_friends_data_rows(user_id: int,
                            auth_token: str,
                            ) -> list[FriendRow]:
    data = requests.get(
        url='https://api.vk.com/method/friends.get/',
        params={'user_id': user_id,
                'v': 5.131,
                'order': 'name',
                'fields': 'bdate, city, country, sex'},
        headers={'Authorization': f'Bearer {auth_token}'},
    )
    return _make_friends_pretty(json.loads(data.content)['response']['items'])


def save_friends_data_rows(friends: Sequence[FriendRow],
                           out_path: str,
                           out_format: Literal['csv', 'tsv', 'json'],
                           ) -> None:
    # may want to use the open-closed principal
    match out_format:
        case 'csv':
            _save_friends_csv(friends, out_path)
        case 'tsv':
            _save_friends_tsv(friends, out_path)
        case 'json':
            _save_friends_json(friends, out_path)


def _save_friends_csv(friends: Sequence[FriendRow],
                      out_path: str
                      ) -> None:
    # need only colum_names and the rows with data only
    with open(f'{out_path}.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, friends[0].keys())
        writer.writeheader()
        writer.writerows(friends)


def _save_friends_tsv(friends: Sequence[FriendRow],
                      out_path: str,
                      ) -> None:
    with open(f'{out_path}.tsv', 'w', encoding='utf-8', newline='') as file:
        writer = tsv.TsvWriter(file)
        writer.line(*friends[0].keys())
        for friend in friends:
            writer.line(*friend.values())


def _save_friends_json(friends: Sequence[FriendRow],
                       out_path: str,
                       ) -> None:
    with open(f'{out_path}.json', 'w', encoding='utf-8', newline='') as file:
        json.dump(friends, fp=file, ensure_ascii=False)


def _make_friends_pretty(friends_lst: list[dict],
                         ) -> list[FriendRow]:
    res = [
        {
            'Имя': friend['first_name'],
            'Фамилия': friend['last_name'],
            'Страна': _get_field(friend, 'country'),
            'Город': _get_field(friend, 'city'),
            'Дата рождения': _get_birthdate(friend),
            'Пол': 'женский' if friend['sex'] == 1 else 'мужской',
        }
        for friend in friends_lst
    ]
    return res


def _get_field(friend: dict,
               field_name: str,
               ) -> str:
    field_value = friend.get(field_name)
    return 'не указано' if field_value is None else field_value['title']


def _get_city(friend: dict) -> str:
    city = friend.get('city')
    return 'не указано' if city is None else city['title']


def _get_birthdate(friend: dict) -> str:
    return friend.get('bdate') or 'не указано'


if __name__ == '__main__':
    main()
