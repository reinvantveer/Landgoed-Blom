import requests

from nextcloud.nextcloud_server import Nextcloud


def load_users(nextcloud: Nextcloud, file_id: str) -> list[dict[str, str]]:
    # Use the ocs API to get the file by id
    resp = requests.get(
        url=f'{nextcloud.server}/ocs/v1.php/cloud/files/{file_id}',
        auth=(nextcloud.username, nextcloud.password),
        headers={'OCS-APIRequest': 'true'}
    )
    resp.raise_for_status()
