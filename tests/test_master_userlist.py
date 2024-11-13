import os

from nextcloud.master_userlist import load_users
from nextcloud.nextcloud_server import Nextcloud


def test_get_master_userlist():
    nc = Nextcloud(username='Admin', password=os.environ['password'], server="https://nextcloud.example.com")
    userlist = load_users("pyproject.toml")