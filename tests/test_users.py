from nextcloud.nextcloud_server import Nextcloud
from nextcloud.users import get_user_ids


def test_get_user_ids():
    nc = Nextcloud()
    user_ids = get_user_ids(nc)

    # Validate that all user ids are email addresses
    for user_id in user_ids:
        assert '@' in user_id
