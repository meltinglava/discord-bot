from typing import Any

import aiohttp

from helpers.config import config


class APIHelper:
    def __init__(self):
        self.base_url = config.EVENT_CALENDAR_URL
        self.headers = {
            'Authorization': f'Bearer {config.EVENT_API_TOKEN}',
            'Accept': 'application/json',
        }

    async def _fetch_data(
        self, endpoint: str, params: dict | None = None
    ) -> list[Any] | None:
        """
        Generic method to fetch data from the API.

        Args:
            endpoint (str): The API endpoint to query.
            params (dict, optional): Query parameters to include in the request.

        Returns:
            Optional[List[Any]]: The parsed JSON response data or None if the request fails.

        """
        url = f'{self.base_url}/{endpoint}'

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    url, headers=self.headers, params=params
                ) as response:
                    if response.status == 200:
                        resp = await response.json()

                        data = resp.get('data', {})
                        if data:
                            return data

                        return resp
                    resp = await response.json()
                    error_message = (
                        resp.get('error')
                        or resp.get('errors')
                        or resp.get('message')
                        or 'Unknown error'
                    )
                    print(
                        f'Error fetching data from {url}. Status code: {response.status} with error message: {error_message}'
                    )
                    return None
            except aiohttp.ClientError as e:
                print(f'HTTP error occurred while accessing {url}: {e}')
                return None

    async def post_data(self, endpoint, params: dict | None = None) -> list[Any] | None:
        """Post data to URL with requried information."""
        url = f'{self.base_url}/{endpoint}'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    url, headers=self.headers, data=params
                ) as response:
                    if response.status == 200:
                        resp = await response.json()
                        data = resp.get('message', '')

                        if data:
                            return True
                    else:
                        resp = await response.json()
                        error_message = (
                            resp.get('error')
                            or resp.get('errors')
                            or resp.get('message')
                            or 'Unknown error'
                        )
                        print(
                            f'Error posting data. Status code: {response.status} with error message: {error_message}',
                            flush=True,
                        )
                        raise Exception(
                            f'API responded with status code {response.status}. Error msg: {error_message}'  # noqa: EM102
                        )
            except aiohttp.ClientError as e:
                print(f'HTTP error occurred while updating staffing message: {e}')

    async def patch_data(
        self, endpoint, params: dict | None = None
    ) -> list[Any] | None:
        """Patch data with specific params to a defined URL."""
        url = f'{self.base_url}/{endpoint}'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(
                    url, headers=self.headers, data=params
                ) as response:
                    if response.status == 200:
                        resp = await response.json()
                        data = resp.get('message', '')

                        if data:
                            return True
                    else:
                        resp = await response.json()
                        error_message = (
                            resp.get('error')
                            or resp.get('errors')
                            or resp.get('message')
                            or 'Unknown error'
                        )
                        print(
                            f'Error patching data. Status code: {response.status} with error message: {error_message}'
                        )
                        raise Exception(
                            f'API responded with status code {response.status}. Error msg: {error_message}'  # noqa: EM102
                        )
            except aiohttp.ClientError as e:
                print(f'HTTP error occurred while updating staffing message: {e}')
                raise Exception(  # noqa: B904
                    f'HTTP error occurred while updating staffing message: {e}'  # noqa: EM102
                )
