import argparse
from argparse import Namespace

from loguru import logger

from nextcloud.auth import generate_password
from nextcloud.mail_server import LandgoedBlomMailServer
from nextcloud.master_userlist import load_users_from_spreadsheet
from nextcloud.nextcloud_server import Nextcloud, NextcloudUser
from nextcloud.users import get_user_ids, create_user, get_user, update_user


def main(args: Namespace) -> None:
    nc = Nextcloud(config_file=args.config)
    # Get the list of users from the Nextcloud server administration
    existing_nextcloud_users = get_user_ids(nc)

    # Load the master user list from the Excel file
    master_user_list = load_users_from_spreadsheet(nc)
    # Extract out the user ids
    master_user_ids = set(master_user_list.keys())

    # Get the list of users from the master user list in the Excel file
    logger.warning('NOTE: The user list is cached, so it may not be up to date')
    logger.warning('Please check the user list before proceeding:')
    for user in master_user_list:
        logger.info(f'{user} ({master_user_list[user]})')

    if not args.yes:
        response = input('Have you checked if the user list is up to date? [y/N]: ')
        if response.lower() != 'y':
            logger.info('Aborting')
            return

    users_not_yet_in_nextcloud = master_user_ids.difference(existing_nextcloud_users)
    mail_server = LandgoedBlomMailServer(config_file=args.config)

    if not args.yes:
        logger.info('The following users will be added to Nextcloud:')
        for user_id in users_not_yet_in_nextcloud:
            display_name = master_user_list[user_id]
            logger.info(f'{display_name} ({user_id})')

        if not args.yes:
            response = input('Do you want to continue? [y/N]: ')
            if response.lower() != 'y':
                logger.info('Aborting')
                return

    for user_id in users_not_yet_in_nextcloud:
        display_name = master_user_list[user_id]

        if args.dry_run:
            logger.info(f'Dry-run: Would have added user {display_name} with id {user_id}')
            continue

        logger.info(f'Adding user: {user_id}')
        user_password = generate_password()

        # Create the user in Nextcloud
        user = NextcloudUser(
            userid=user_id,
            email=user_id,
            password=user_password,
            displayName=display_name
        )
        create_user(nc, user)

        # Send the user an email with the login information
        mail_server.send_create_mail(
            display_name=display_name,
            user_name=user_id,
            user_email=user_id,
            user_password=user_password
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update users in the Nextcloud database')

    dry_run_help = 'Do not actually update the users'
    parser.add_argument('--dry-run', action='store_true', help=dry_run_help, default=False)

    config_help = 'Path to the configuration file'
    parser.add_argument('--config', help=config_help, default='pyproject.toml')

    # For automated scripts that need to update the users
    config_help = 'Are you sure you want to update the users?'
    parser.add_argument('--yes', help=config_help, action='store_true', default=False)

    args = parser.parse_args()
    main(args)