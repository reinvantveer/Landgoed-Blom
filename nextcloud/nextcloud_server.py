import os
import tomllib
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Nextcloud:
    """Dataclass for Nextcloud server configuration"""
    config_file: str = 'pyproject.toml'
    config: dict[str, str] = field(default_factory=dict)
    server: str = ''
    username: str = ''
    password: str = ''

    def __post_init__(self) -> None:
        with open(self.config_file, 'rb') as f:
            self.config = tomllib.load(f)['tool']['landgoed-blom']

        self.server = self.config['server_url']
        self.username = self.config['user']
        self.password = os.environ['NEXTCLOUD_PASSWORD']
        self.file_path = self.config['user_list_file_path']

@dataclass(kw_only=True)
class NextcloudUser:
    """Dataclass for Nextcloud user"""
    userid: str
    email: str
    password: str
    displayName: str

    def __post_init__(self) -> None:
        if '@' not in self.userid:
            raise ValueError(f'User id {self.userid} is not an email address')
        if '@' not in self.email:
            raise ValueError(f'Email {self.email} is not a valid email address')
