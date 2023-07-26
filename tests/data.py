# FOR test_data_loaders.py:
import common

VALID_JSON = b'{"response":{"count":178,"items":[{"id":562079661,"bdate":"26.5.1995","city":{"id":144,"title":"\xd0\xa2\xd0\xbe\xd0\xbc\xd1\x81\xd0\xba"},"country":{"id":1,"title":"\xd0\xa0\xd0\xbe\xd1\x81\xd1\x81\xd0\xb8\xd1\x8f"},"track_code":"ba7daa43Q8XVhXKRfdKf6lZxibQjtm5IUEa6K6-8pkd4sLC72qIuro3kT8Uo0c7ub_4kAZPeHVxJSq1Fy8_5","sex":2,"first_name":"Abdullah Bin","last_name":"Firoz","can_access_closed":true,"is_closed":false},{"id":430984321,"bdate":"10.9","country":{"id":1,"title":"\xd0\xa0\xd0\xbe\xd1\x81\xd1\x81\xd0\xb8\xd1\x8f"},"track_code":"73ba22cf_tuLRJ8x9XExYkiY0cTJbh2VEVIqNpZhe7dcr_b6_BuTsNJ08GaleTtpfRJ4cXkGboEIXj1Y8hIk","sex":1,"first_name":"Alena","last_name":"Kulishova","can_access_closed":true,"is_closed":true},{"id":411295345,"track_code":"e1d31ff6HYQ96F3vsORtvv60B-z5ts4hUW82j_1uhDHtPU_8yihw7zSJbO-44G_hyT6oXUnevTVIYyHhmR3b","sex":2,"first_name":"Dionis","last_name":"Lez","can_access_closed":true,"is_closed":true},{"id":502390027,"bdate":"25.9","city":{"id":144,"title":"\xd0\xa2\xd0\xbe\xd0\xbc\xd1\x81\xd0\xba"},"country":{"id":1,"title":"\xd0\xa0\xd0\xbe\xd1\x81\xd1\x81\xd0\xb8\xd1\x8f"},"track_code":"310cd2c0ek67zdEiWFfnzqmjIiNkIyFW_eAbasQ6aFmyM9Fxef0XJbT17SBRXeSWmiqLkNRLUkLk7AwEoEk3","sex":1,"first_name":"Elena","last_name":"Rodionova","can_access_closed":true,"is_closed":false},{"id":489365669,"bdate":"1.7.1986","track_code":"f5f95a26o0tvS4uy1EOpKjHcNUFqettzb8cEHOy-9Zd6-5gKeKzOIDNyu7WIHKx6AFOY_NoSqGd2yxNyiM2q","sex":2,"first_name":"Mohamed","last_name":"Shahat-Ahmed","can_access_closed":true,"is_closed":false}]}}'
BAD_TOKEN_JSON = b'{"error":{"error_code":5,"error_msg":"User authorization failed: invalid access_token (4).","request_params":[{"key":"v","value":"5.131"},{"key":"order","value":"name"},{"key":"fields","value":"bdate, city, country, sex"},{"key":"offset","value":"0"},{"key":"count","value":"5"},{"key":"method","value":"friends.get"},{"key":"oauth","value":"1"}]}}'
BAD_USER_ID_JSON = b'{"error":{"error_code":18,"error_msg":"User was deleted or banned","request_params":[{"key":"user_id","value":"4345"},{"key":"v","value":"5.131"},{"key":"order","value":"name"},{"key":"fields","value":"bdate, city, country, sex"},{"key":"offset","value":"0"},{"key":"count","value":"5"},{"key":"method","value":"friends.get"},{"key":"oauth","value":"1"}]}}'
CLOSED_USER_ACCOUNT_JSON = b'{"error":{"error_code":30,"error_msg":"This profile is private","request_params":[{"key":"user_id","value":"35184846"},{"key":"v","value":"5.131"},{"key":"order","value":"name"},{"key":"fields","value":"bdate, city, country, sex"},{"key":"offset","value":"0"},{"key":"count","value":"5"},{"key":"method","value":"friends.get"},{"key":"oauth","value":"1"}]}}'
INVALID_STRUCTURE_JSON = b'{"response":{"count":178,"items":[{"id":562079661,"bdate":"26.5.1995","city":{"id":144,"title":"\xd0\xa2\xd0\xbe\xd0\xbc\xd1\x81\xd0\xba"},"country":{"id":1,"title":"\xd0\xa0\xd0\xbe\xd1\x81\xd1\x81\xd0\xb8\xd1\x8f"},"track_code":"ba7daa43Q8XVhXKRfdKf6lZxibQjtm5IUEa6K6-8pkd4sLC72qIuro3kT8Uo0c7ub_4kAZPeHVxJSq1Fy8_5","sex":2,"first_name":"Abdullah Bin","last_name":"Firoz","can_access_closed":true,"is_closed":false},{"id":430984321,"bdate":"10.9","country":{"id":1,"title":"\xd0\xa0\xd0\xbe\xd1\x81\xd1\x81\xd0\xb8\xd1\x8f"},"track_code":"73ba22cf_tuLRJ8x9XExYkiY0cTJbh2VEVIqNpZhe7dcr_b6_BuTsNJ08GaleTtpfRJ4cXkGboEIXj1Y8hIk","sex":1,"first_name":"Alena","last_name":"Kulishova","can_access_closed":true,"is_closed":true},{"id":411295345,"track_code":"e1d31ff6HYQ96F3vsORtvv60B-z5ts4hUW82j_1uhDHtPU_8yihw7zSJbO-44G_hyT6oXUnevTVIYyHhmR3b","sex":2,"first_name":"Dionis","last_name":"Lez","can_access_closed":true,"is_closed":true},{"id":502390027,"bdate":"25.9","city":{"id":144,"title":"\xd0\xa2\xd0\xbe\xd0\xbc\xd1\x81\xd0\xba"},"country":{"id":1,"title":"\xd0\xa0\xd0\xbe\xd1\x81\xd1\x81\xd0\xb8\xd1\x8f"},"track_code":"310cd2c0ek67zdEiWFfnzqmjIiNkIyFW_eAbasQ6aFmyM9Fxef0XJbT17SBRXeSWmiqLkNRLUkLk7AwEoEk3","sex":1,"first_name":"Elena","last_name":"Rodionova","can_access_closed":true,"is_closed":false},{"id":489365669,"bdate":"1.7.1986","track_code":"f5f95a26o0tvS4uy1EOpKjHcNUFqettzb8cEHOy-9Zd6-5gKeKzOIDNyu7WIHKx6AFOY_NoSqGd2yxNyiM2q","sex":"abc","first_name":"Mohamed","last_name":"Shahat-Ahmed","can_access_closed":true,"is_closed":false}]}}'
UNKNOWN_ERROR_CODE_JSON = b'{"error":{"error_code":13,"error_msg":"User authorization failed: invalid access_token (4).","request_params":[{"key":"v","value":"5.131"},{"key":"order","value":"name"},{"key":"fields","value":"bdate, city, country, sex"},{"key":"offset","value":"0"},{"key":"count","value":"5"},{"key":"method","value":"friends.get"},{"key":"oauth","value":"1"}]}}'

VALID_RESULT = [
    {'Имя': 'Abdullah Bin', 'Фамилия': 'Firoz', 'Страна': 'Россия', 'Город': 'Томск', 'Дата рождения': '1995-05-26',
     'Пол': 'мужской'},
    {'Имя': 'Alena', 'Фамилия': 'Kulishova', 'Страна': 'Россия', 'Город': 'не указано', 'Дата рождения': '10-09',
     'Пол': 'женский'},
    {'Имя': 'Dionis', 'Фамилия': 'Lez', 'Страна': 'не указано', 'Город': 'не указано', 'Дата рождения': 'не указано',
     'Пол': 'мужской'},
    {'Имя': 'Elena', 'Фамилия': 'Rodionova', 'Страна': 'Россия', 'Город': 'Томск', 'Дата рождения': '25-09',
     'Пол': 'женский'},
    {'Имя': 'Mohamed', 'Фамилия': 'Shahat-Ahmed', 'Страна': 'не указано', 'Город': 'не указано',
     'Дата рождения': '1986-07-01', 'Пол': 'мужской'}
]


class MockResponse:
    content: bytes

    def __init__(self,
                 content: bytes,
                 ) -> None:
        self.content = content


VALID_RESPONSE = MockResponse(VALID_JSON)
BAD_TOKEN_RESPONSE = MockResponse(BAD_TOKEN_JSON)
BAD_USER_ID_RESPONSE = MockResponse(BAD_USER_ID_JSON)
CLOSED_USER_ACCOUNT_RESPONSE = MockResponse(CLOSED_USER_ACCOUNT_JSON)
INVALID_STRUCTURE_RESPONSE = MockResponse(INVALID_STRUCTURE_JSON)
UNKNOWN_ERROR_CODE_RESPONSE = MockResponse(UNKNOWN_ERROR_CODE_JSON)

# FOR test_savers.py:
SAVE_DATA1: list[common.FriendDataPretty] = [
    {'Имя': 'Андрей', 'Фамилия': 'Гунько', 'Страна': 'Россия',
     'Город': 'Томск', 'Дата рождения': '06-10', 'Пол': 'мужской'},
    {'Имя': 'Анна', 'Фамилия': 'Кузнецова', 'Страна': 'Россия',
     'Город': 'Томск', 'Дата рождения': '27-10', 'Пол': 'женский'},
    {'Имя': 'Анна', 'Фамилия': 'Юмашева', 'Страна': 'Россия',
     'Город': 'Томск', 'Дата рождения': 'не указано', 'Пол': 'женский'}
]
