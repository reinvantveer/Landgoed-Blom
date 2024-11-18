from dataclasses import asdict
from typing import Any

import requests

from nextcloud.nextcloud_server import Nextcloud, NextcloudUser


def get_user(nextcloud: Nextcloud, user_id: str) -> dict[str, str]:
    """Read out a user in Nextcloud"""
    resp = requests.get(
        url=f'{nextcloud.server}/ocs/v1.php/cloud/users/{user_id}?format=json',
        auth=(nextcloud.username, nextcloud.password),
        headers={'OCS-APIRequest': 'true'}
    )
    resp.raise_for_status()
    user = resp.json()

    return user  # type: ignore


def get_user_ids(nextcloud: Nextcloud) -> set[str]:
    """Read out the users in Nextcloud"""
    resp = requests.get(
        url=f'{nextcloud.server}/ocs/v1.php/cloud/users?format=json',
        auth=(nextcloud.username, nextcloud.password),
        headers={'OCS-APIRequest': 'true'}
    )
    resp.raise_for_status()
    users = resp.json()

    usernames = users['ocs']['data']['users']
    # Lowercase all user ids
    usernames = {user.lower() for user in usernames}

    # We always use mail addresses as the user id
    return set(user for user in usernames if '@' in user)


def create_user(nextcloud: Nextcloud, user: NextcloudUser) -> None:
    """Create a user in Nextcloud"""
    resp = requests.post(
        url=f'{nextcloud.server}/ocs/v1.php/cloud/users?format=json',
        json=asdict(user),
        auth=(nextcloud.username, nextcloud.password),
        headers={
            'OCS-APIRequest': 'true',
            'Content-Type': 'application/json'
        }
    )
    resp.raise_for_status()
    result = resp.json()

    if result['ocs']['meta']['status'] != 'ok':
        raise ValueError(result['ocs']['meta']['message'])

def update_user(nextcloud: Nextcloud, user: NextcloudUser) -> None:
    resp = requests.put(
        url=f'{nextcloud.server}/ocs/v1.php/cloud/users/{user.userid}',
        json=asdict(user),
        auth=(nextcloud.username, nextcloud.password),
        headers={
            'OCS-APIRequest': 'true',
            'Content-Type': 'application/json'
        }
    )
    resp.raise_for_status()
    result = resp.json()

    if result['ocs']['meta']['status'] != 'ok':
        raise ValueError(result['ocs']['meta']['message'])


def delete_user(nextcloud: Nextcloud, user: NextcloudUser) -> None:
    resp = requests.delete(
        url=f'{nextcloud.server}/ocs/v1.php/cloud/users/{user.userid}?format=json',
        auth=(nextcloud.username, nextcloud.password),
        headers={'OCS-APIRequest': 'true'}
    )
    resp.raise_for_status()
    result = resp.json()

    if result['ocs']['meta']['status'] != 'ok':
        raise ValueError(result['ocs']['meta']['message'])
