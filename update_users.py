import argparse
from argparse import Namespace

from loguru import logger

from nextcloud.auth import generate_password
from nextcloud.master_userlist import load_users_from_spreadsheet
from nextcloud.nextcloud_server import Nextcloud
from nextcloud.users import get_user_ids, create_user, get_user, update_user


def main(args: Namespace) -> None:
    nc = Nextcloud(config_file=args.config)
    # Get the list of users from the Nextcloud server administration
    existing_nextcloud_users = get_user_ids(nc)
    # Get the list of users from the master user list in the Excel file
    master_user_list = load_users_from_spreadsheet(nc)
    # Extract out the user ids
    master_user_ids = set(master_user_list.keys())

    users_not_yet_in_nextcloud = master_user_ids.difference(existing_nextcloud_users)

    for user_id in users_not_yet_in_nextcloud:
        if args.dry_run:
            logger.info(f'Dry-run: Would have added user {user_id}')
            continue

        logger.info(f'Adding user: {user_id}')
        user = {
            'userid': user_id,
            'password': generate_password(),
            'displayName': user_id
        }
        create_user(nc, user)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update users in the Nextcloud database')

    dry_run_help = 'Do not actually update the users'
    parser.add_argument('--dry-run', action='store_true', help=dry_run_help, default=True)

    config_help = 'Path to the configuration file'
    parser.add_argument('--config', help=config_help, default='pyproject.toml')

    args = parser.parse_args()
    main(args)