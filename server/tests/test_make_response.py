import pytest
from datetime import datetime
from protocol import make_response


@pytest.fixture
def expected_action():
    return 'test'

@pytest.fixture
def expected_code():
    return 200

@pytest.fixture
def expected_data():
    return 'Some data'

# ACTION = 'test'
# CODE = 200
# DATA = 'Some data'

@pytest.fixture
def initial_response(expected_action, expected_code, expected_data):
    return {
        'action': expected_action,
        'time' : datetime.now().timestamp(),
        'data': expected_data
        }

# RESPONSE = {
#     'action': ACTION,
#     'time' : datetime.now().timestamp(),
#     'code': CODE,
#     'data': DATA
# }

def test_make_response_action(initial_response, expected_action, expected_code, expected_data):
    actual_response = make_response(initial_response, expected_code, expected_data)
    assert actual_response.get('action') == expected_action

def test_make_response_code(initial_response, expected_code, expected_data):
    actual_response = make_response(initial_response, expected_code, expected_data)
    assert actual_response.get('code') == expected_code

def test_make_response_data(initial_response, expected_data):
    actual_response = make_response(initial_response, expected_code, expected_data)
    assert actual_response.get('data') == expected_data 
