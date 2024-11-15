from nextcloud.master_userlist import load_users_from_spreadsheet
from nextcloud.nextcloud_server import Nextcloud


def test_get_master_userlist():
    nc = Nextcloud()
    user_list = load_users_from_spreadsheet(nc)

    # Make sure that all user ids are email addresses
    for user_id in user_list:
        assert '@' in user_id
