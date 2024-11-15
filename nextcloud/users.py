import requests

from nextcloud.nextcloud_server import Nextcloud


def create_user(nextcloud: Nextcloud, user: dict) -> None:
    resp = requests.post(
        url=f'{nextcloud.server}/ocs/v1.php/cloud/users',
        json=user,
        auth=(nextcloud.username, nextcloud.password),
        headers={
            'OCS-APIRequest': 'true',
            'Content-Type': 'application/json'
        }
    )
    resp.raise_for_status()


def update_user(nextcloud: Nextcloud, user: dict) -> None:
    resp = requests.put(
        url=f'{nextcloud.server}/ocs/v1.php/cloud/users/{user["id"]}',
        json=user,
        auth=(nextcloud.username, nextcloud.password),
        headers={
            'OCS-APIRequest': 'true',
            'Content-Type': 'application/json'
        }
    )
    resp.raise_for_status()


def get_user(nextcloud: Nextcloud, user_id) -> dict:
    resp = requests.get(
        url=f'{nextcloud.server}/ocs/v1.php/cloud/users/{user_id}?format=json',
        auth=(nextcloud.username, nextcloud.password),
        headers={'OCS-APIRequest': 'true'}
    )
    resp.raise_for_status()
    user = resp.json()

    return user


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

    # We always use mail addresses as the user id
    return set(user for user in usernames if '@' in user)
