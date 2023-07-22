import json
import requests
from datetime import datetime
from typing import Literal

from common import FriendRow


class VkDataLoader:
    _API_VERSION = 5.131
    _GENDER_MAPPER: dict[int, Literal['мужской', 'женский']] = {
        1: 'женский',
        2: 'мужской',
    }

    def load_friends_data(self,
                          user_id: int,
                          auth_token: str,
                          order: str = 'name',
                          fields: str = 'bdate, city, country, sex',
                          ) -> list[FriendRow]:
        data = requests.get(
            url='https://api.vk.com/method/friends.get/',
            params={'user_id': user_id,
                    'v': self._API_VERSION,
                    'order': order,
                    'fields': fields},
            headers={'Authorization': f'Bearer {auth_token}'},
        )
        return self._convert_friends_data(json.loads(data.content)['response']['items'])

    def _convert_friends_data(self,
                              friends_raw: list[dict],
                              ) -> list[FriendRow]:
        res = [
            {
                'Имя': self._get_field_or_not_stated(friend_raw, 'first_name'),
                'Фамилия': self._get_field_or_not_stated(friend_raw, 'last_name'),
                'Страна': self._get_field_or_not_stated_from_nested(friend_raw, 'country'),
                'Город': self._get_field_or_not_stated_from_nested(friend_raw, 'city'),
                'Дата рождения': self._get_birthdate(friend_raw),
                'Пол': self._get_gender(friend_raw)
            }
            for friend_raw in friends_raw
        ]
        return res

    def _get_gender(self,
                    friend: FriendRow,
                    ) -> Literal['мужской', 'женский', 'не указано']:
        vk_format_gender = self._get_field_or_not_stated(friend, 'sex')
        if vk_format_gender is None:
            return 'не указано'

        return self._GENDER_MAPPER[vk_format_gender]

    @staticmethod
    def _get_field_or_not_stated(friend: dict,
                                 field_name: str
                                 ) -> str | int:
        return friend.get(field_name) or 'не указано'

    @staticmethod
    def _get_field_or_not_stated_from_nested(friend: dict,
                                             field_name: str,
                                             ) -> str:
        field_value = friend.get(field_name)
        return 'не указано' if field_value is None else field_value['title']

    def _get_birthdate(self,
                       friend: dict,
                       ) -> str:
        raw_birthdate = self._get_field_or_not_stated(friend, 'bdate')
        if raw_birthdate == 'не указано':
            return 'не указано'

        return self._convert_to_iso(raw_birthdate)

    @staticmethod
    def _convert_to_iso(date_str):
        for format in ("%d.%m", "%d.%m.%Y"):
            try:
                date_obj = datetime.strptime(date_str, format)
                if date_obj.year == 1900:
                    return date_obj.strftime("%d-%m")
                else:
                    return date_obj.date().isoformat()
            except ValueError:
                continue
