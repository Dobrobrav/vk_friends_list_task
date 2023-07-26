import pydantic_core
import pytest
import requests.exceptions

import data_loaders
import data
import common


@pytest.fixture
def vk_data_loader():
    return data_loaders.VkDataLoader()


@pytest.mark.parametrize(
    "user_id, access_token, order, fields, page, limit, response_data, expected_result",
    [
        # Test case 1: everything valid
        (12345, 'some-valid-token', 'name', 'bdate, city, country, sex', None, None,
         data.VALID_RESPONSE, data.VALID_RESULT)

        # other test cases ...
    ]
)
def test_load_friends_data(vk_data_loader: data_loaders.VkDataLoader,
                           user_id, access_token, order, fields, page,
                           limit, response_data, expected_result) -> None:
    """ Testing non-exceptional cases """
    # mocking the '_request_friends_data' func, which accesses VK API,
    # because the response of that function is not consistent,
    # plus don't fancy storing access point in the code, so I use mocking func
    vk_data_loader._request_friends_data = (
        lambda auth_token, user_id, order, fields, page, limit: response_data
    )
    actual_result = vk_data_loader.load_friends_data(
        user_id, access_token, order, fields, page, limit
    )

    assert actual_result == expected_result


@pytest.mark.parametrize(
    "user_id, access_token, order, fields, page, limit, response_data, expected_error, is_connection_bad",
    [
        # Test case 1: Invalid token
        (34535, 'some-invalid-token', 'name', 'bdate, city, country, sex', None, None,
         data.BAD_TOKEN_RESPONSE, common.InvalidInputError, False),

        # Test case 2: valid token, invalid user_id
        (123, 'some-valid-token', 'name', 'bdate, city, country, sex', None, None,
         data.BAD_USER_ID_RESPONSE, common.InvalidInputError, False),

        # Test case 3: Valid token, Valid user id, Profile is closed
        (34562, 'some-valid-token', 'name', 'bdate, city, country, sex', None, None,
         data.CLOSED_USER_ACCOUNT_RESPONSE, common.ClosedVkProfileError, False),

        # Test case 4: Valid token, Valid user_id, Profile is open,
        # (for some reason, vk sends wrong structure)
        (34562, 'some-valid-token', 'name', 'bdate, city, country, sex', None, None,
         data.INVALID_STRUCTURE_RESPONSE, pydantic_core.ValidationError, False),

        # Test case 5: everything is valid, unknown value of 'error' field in vk response
        (34562, 'some-valid-token', 'name', 'bdate, city, country, sex', None, None,
         data.UNKNOWN_ERROR_CODE_RESPONSE, common.UnexpectedVkError, False),

        # Test case 6: bad network connection
        (34562, 'some-valid-token', 'name', 'bdate, city, country, sex', None, None,
         data.UNKNOWN_ERROR_CODE_RESPONSE, requests.exceptions.ConnectionError, True),
    ]
)
def test_load_friends_data_errors(
        vk_data_loader: data_loaders.VkDataLoader,
        user_id, access_token, order, fields, page,
        limit, response_data, expected_error, is_connection_bad,
) -> None:
    """ Testing exceptional cases """
    # mocking the '_request_friends_data' func, which accesses VK API
    def mock_func(auth_token, user_id, order, fields, page, limit):
        """ raise ConnectionError if network connection is bad """
        if is_connection_bad:
            raise requests.exceptions.ConnectionError()
        return response_data

    vk_data_loader._request_friends_data = mock_func

    with pytest.raises(expected_error):
        vk_data_loader.load_friends_data(
            user_id, access_token, order, fields, page, limit
        )


if __name__ == '__main__':
    pytest.main()
