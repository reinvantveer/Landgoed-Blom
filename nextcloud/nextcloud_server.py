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

    def __post_init__(self):
        with open(self.config_file, 'rb') as f:
            self.config = tomllib.load(f)['tool']['landgoed-blom']

        self.server = self.config['server_url']
        self.username = self.config['user']
        self.password = os.environ['PASSWORD']
