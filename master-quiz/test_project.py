import pytest
import json
from project import get_api_data, get_level, start_or_exit_prompt


# test wheather to start or exit program
@pytest.mark.parametrize(
    "user_input, expected_result",
    [
        ("y", True),
        ("n", False),
    ],
)
def test_start_or_exit_prompt(monkeypatch, user_input, expected_result):
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    assert start_or_exit_prompt(True) == expected_result


# test to get the difficulty level
@pytest.mark.parametrize(
    "user_input, expected_result",
    [
        ("1", "easy"),
        ("mixed", ""),
    ],
)
def test_get_level(monkeypatch, user_input, expected_result):
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    result = get_level()
    assert result == expected_result


# test the api
def test_get_api_data(requests_mock):
    # Mock an API response
    mock_data = {"results": ["mocked_data"]}
    requests_mock.get(
        "https://opentdb.com/api.php?amount=10&difficulty=easy",
        text=json.dumps(mock_data),
    )
    level = "easy"
    result = get_api_data(level)
    assert result == mock_data["results"]
