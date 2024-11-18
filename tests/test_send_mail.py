from nextcloud.auth import generate_password
from nextcloud.mail_server import LandgoedBlomMailServer


def test_mail() -> None:
    mailserver = LandgoedBlomMailServer('pyproject.toml')
    mailserver.send_create_mail(
        display_name='Test User',
        user_name='test',
        user_email='pioniersgroep@buitenhuisblom.nl',
        user_password=generate_password(length=12),
    )
