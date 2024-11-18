from nextcloud.auth import generate_password
from nextcloud.nextcloud_server import Nextcloud, NextcloudUser
from nextcloud.users import get_user_ids, create_user, delete_user


def test_get_user_ids():
    nc = Nextcloud()
    user_ids = get_user_ids(nc)

    # Validate that all user ids are email addresses
    for user_id in user_ids:
        assert '@' in user_id

# Integration tests
def test_add_user():
    nc = Nextcloud()
    user = 'pioniersgroep@buitenhuisblom.nl'
    user = NextcloudUser(userid=user, email=user, password=generate_password(), displayName='Test User')
    create_user(nc, user)
    user_ids = get_user_ids(nc)
    assert user.userid in user_ids

    # Clean up
    delete_user(nc, user)
    user_ids = get_user_ids(nc)
    assert user.userid not in user_ids

