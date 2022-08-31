"""Test cases for the wikipedia module."""
from unittest.mock import Mock

import click

from hypermodern_python_example import wikipedia


# testing that the language option is working
def test_random_page_uses_given_language(mock_requests_get: Mock) -> None:
    """It selects the specified Wikipedia language edition"""
    wikipedia.random_page(language="de")
    args, _ = mock_requests_get.call_args
    assert "de.wikipedia.org" in args[0]
