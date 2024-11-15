import pandas
import requests

from nextcloud.nextcloud_server import Nextcloud


def load_users_from_spreadsheet(nextcloud: Nextcloud) -> dict[str, str]:
    """
    Load the user ids from the spreadsheet

    Args:
        nextcloud: The Nextcloud object

    Returns:
        A dictionary with the user ids as keys and the display names as values
    """

    # Use the WebDAV API to get the file by id

    resp = requests.get(
        url=f'{nextcloud.server}/remote.php/dav/files/{nextcloud.username}/{nextcloud.file_path}',
        auth=(nextcloud.username, nextcloud.password),
        headers={'OCS-APIRequest': 'true'}
    )
    resp.raise_for_status()

    # Open the Excel file and read the users
    df = pandas.read_excel(resp.content)
    # We always use mail addresses as the user id
    mail_addresses = df['Mail'].filter(regex='@', axis=0)

    return set(mail_addresses)
