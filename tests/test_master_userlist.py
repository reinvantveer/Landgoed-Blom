import os

from nextcloud.master_userlist import load_users_from_spreadsheet
from nextcloud.nextcloud_server import Nextcloud


def test_get_master_userlist():
    nc = Nextcloud()
    userlist = load_users_from_spreadsheet(nc)

    # Make sure that all user ids are email addresses
    for user_id in userlist:
        assert '@' in user_id
