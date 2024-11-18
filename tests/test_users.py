from nextcloud.nextcloud_server import Nextcloud
from nextcloud.users import get_user_ids, create_user


def test_get_user_ids():
    nc = Nextcloud()
    user_ids = get_user_ids(nc)

    # Validate that all user ids are email addresses
    for user_id in user_ids:
        assert '@' in user_id

# Integration tests
def test_add_user():
    nc = Nextcloud()
    user = {
        'userid': 'pioniersgroep@buitenhuisblom.nl',
        'password': 'test_password',
        'displayName': 'Test User'
    }
    create_user(nc, user)
