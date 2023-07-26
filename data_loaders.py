import json
import pydantic_core
import requests
from datetime import datetime
from typing import Literal, TypeVar

import common
import log_utils

T = TypeVar('T')


class VkDataLoader:
    _API_VERSION = 5.131
    _GENDER_MAPPER: dict[Literal[1, 2], Literal['мужской', 'женский']] = {
        1: 'женский',
        2: 'мужской',
    }
    _TOTAL_LIMIT = 100_000
    _PAGE_LIMIT = 14

    def load_friends_data(self,
                          user_id: int | None,
                          access_token: str,
                          order: str = 'name',
                          fields: str = 'bdate, city, country, sex',
                          page: int | None = None,
                          limit: int | None = None,
                          ) -> list[common.FriendDataPretty]:
        log_utils.log_start_loading_friends_data(user_id)

        raw_response = self._request_friends_data(
            auth_token=access_token,
            user_id=user_id,
            order=order,
            fields=fields,
            page=page,
            limit=limit,
        )
        validated_data = self._validate_response(raw_response)
        friends_data_pretty = self._convert_friends_data_to_pretty(
            friends_data=validated_data.response.items
        )

        log_utils.log_finish_loading_friends_data(user_id)

        return friends_data_pretty

    def _request_friends_data(self,
                              auth_token: str,
                              user_id: int,
                              order: str,
                              fields: str,
                              page: int | None = None,
                              limit: int | None = None,
                              ) -> requests.Response:
        log_utils.log_start_http_request(
            url='https://api.vk.com/method/friends.get/'
        )

        request_raw = requests.get(
            url='https://api.vk.com/method/friends.get/',
            params={
                'user_id': user_id,
                'v': self._API_VERSION,
                'order': order,
                'fields': fields,
                'offset': self._calc_offset(page, limit),
                'count': self._calc_count(limit),
            },
            headers={'Authorization': f'Bearer {auth_token}'},
        )

        log_utils.log_finish_http_request(
            url='https://api.vk.com/method/friends.get/'
        )

        return request_raw

    @staticmethod
    def _validate_response(response: requests.Response,
                           ) -> common.ResponseWrapper | None:
        log_utils.log_start_validating_response()

        if 'error' in (content := json.loads(response.content)):
            #
            match error_code := content['error']['error_code']:
                case 5:
                    raise common.InvalidInputError(
                        arg_name='access_token',
                        expected_value_descr='valid vk access token',
                        log_error_descr='Invalid vk access token',
                    )
                case 18:
                    raise common.InvalidInputError(
                        arg_name='user_id',
                        expected_value_descr='valid vk user id',
                        log_error_descr='Invalid vk user id'
                    )
                case 30:
                    raise common.ClosedVkProfileError()
                case _:
                    raise common.UnexpectedVkError(f"Error code: {error_code}")

        try:
            validated_data = common.ResponseWrapper.model_validate_json(
                response.content
            )
        except pydantic_core.ValidationError:
            raise

        if len(validated_data.response.items) == 0:
            print('No friends found. Either you don\'t have vk friends , '
                  'or the <page> or/and <limit> arguments are too high')

        log_utils.log_finish_validating_response()

        return validated_data

    def _calc_offset(self,
                     page: int | None,
                     limit: int | None,
                     ) -> int:
        if page is None:
            return 0
        else:
            return (limit or self._PAGE_LIMIT) * (page - 1)

    def _calc_count(self,
                    limit: int | None,
                    ) -> int:
        if limit is None:
            return self._TOTAL_LIMIT
        else:
            return limit

    def _convert_friends_data_to_pretty(self,
                                        friends_data: list[common.FriendData],
                                        ) -> list[common.FriendDataPretty]:
        res = [
            {
                'Имя': self._get_value_or_empty(friend_data.first_name),
                'Фамилия': self._get_value_or_empty(friend_data.last_name),
                'Страна': self._get_field_or_empty_from_nested(
                    friend_data.country
                ),
                'Город': self._get_field_or_empty_from_nested(
                    friend_data.city
                ),
                'Дата рождения': self._get_birthdate(friend_data),
                'Пол': self._get_gender(friend_data)
            }
            for friend_data in friends_data
        ]
        return res

    def _get_gender(self,
                    friend: common.FriendData,
                    ) -> Literal['мужской', 'женский', 'не указано']:
        vk_format_gender = self._get_value_or_empty(friend.sex)
        if vk_format_gender is None:
            return 'не указано'

        return self._GENDER_MAPPER[vk_format_gender]

    @staticmethod
    def _get_value_or_empty(value: T,
                            ) -> Literal['не указано'] | T:
        return value or 'не указано'

    @staticmethod
    def _get_field_or_empty_from_nested(
            nested_value: common.City | common.Country,
    ) -> str:
        return 'не указано' if nested_value is None else nested_value.title

    def _get_birthdate(self,
                       friend: common.FriendData,
                       ) -> str:
        raw_birthdate = self._get_value_or_empty(friend.bdate)
        if raw_birthdate == 'не указано':
            return 'не указано'

        return self._convert_to_iso(raw_birthdate)

    @staticmethod
    def _convert_to_iso(date_str):
        for format in ("%d.%m", "%d.%m.%Y"):
            # try converting date to on of the formats
            try:
                date_obj = datetime.strptime(date_str, format)
                # if format '%d.%m', 1900 year is automatically assigned. not good
                if date_obj.year == 1900:
                    return date_obj.strftime("%d-%m")
                else:
                    return date_obj.date().isoformat()
            # if conversion fails, try the other format
            except ValueError:
                continue
