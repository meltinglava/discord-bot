from typing import Any

import aiohttp

from helpers.config import config


class Roles:
    """Helper class to interact with the API for roles and training data."""

    def __init__(self) -> None:
        self.base_url = config.CC_API_URL
        self.headers = {
            'Authorization': f'Bearer {config.CC_API_TOKEN}',
            'Accept': 'application/json',
        }

    async def fetch_data(
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
                        data = await response.json()
                        return data.get('data', [])
                    print(
                        f'Error fetching data from {url}. Status code: {response.status}'
                    )
                    return None

            except aiohttp.ClientError as e:
                print(f'HTTP error occurred while accessing {url}: {e}')
                return None

    async def get_roles(self) -> list[Any] | None:
        """
        Fetch all users with their roles from the API.

        Returns:
            Optional[List[Any]]: A list of users and their roles or None if the request fails.

        """
        return await self.fetch_data('users', params={'include[]': 'roles'})

    async def get_training(self) -> list[Any] | None:
        """
        Fetch all users with their training data from the API.

        Returns:
            Optional[List[Any]]: A list of users and their training data or None if the request fails.

        """
        return await self.fetch_data('users', params={'include[]': 'training'})

    async def get_endorsement(self) -> dict | None:
        """
        Fetch all users with their endorsement data from the API.

        Returns:
            Optional[dict]: The visiting endorsement data if valid, or None otherwise.

        """
        return await self.fetch_data('users', params={'include[]': 'endorsements'})

    async def get_atc_activity(self) -> dict | None:
        """
        Fetch all users with their endorsement data from the API.

        Returns:
            Optional[dict]: The visiting endorsement data if valid, or None otherwise.

        """
        params = {
            'include[]': [
                'allUsers',
                'activeAreas',
            ],
            'onlyAtcActive': 1,
        }

        return await self.fetch_data('users', params=params)
