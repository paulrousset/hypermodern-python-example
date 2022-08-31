"""Package wide test fixtures"""
from unittest.mock import Mock

from _pytest.config import Config

import pytest


@pytest.fixture
def mock_requests_get(mocker: Mockfixture) -> Mock:
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock


def pytest_configure(config: Config):
    """Pytest configuration hook"""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
