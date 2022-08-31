"""Client for the Wikipedia REST API, version 1."""

import click
import requests

@dataclass
class Page:
    """Page resource.
    Attributes:
        title: The title of the Wikipedia page.
        extract: A plain text summary.
    """
    title: str
    extract: str

API_URL = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"


def random_page(language: str = "en") -> Page:
    """Return a random page.
    Performs a GET request to the /page/random/summary endpoint.
    Args:
        language: The Wikipedia language edition. By default, the
            English Wikipedia is used ("en").
    Returns:
        A page resource.
    Raises:
        ClickException: The HTTP request failed or the HTTP response
            contained an invalid body.
"""
    url = API_URL.format(language=language)
    try:
        with requests.get(url) as response:
            response.raise_for_status()
            return response.json()
    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message) from None
