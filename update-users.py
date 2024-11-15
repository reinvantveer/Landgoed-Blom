import argparse
from argparse import Namespace

from loguru import logger

from nextcloud.auth import generate_password
from nextcloud.master_userlist import load_users_from_spreadsheet
from nextcloud.nextcloud_server import Nextcloud
from nextcloud.users import get_user_ids, create_user, get_user, update_user


def main(args: Namespace) -> None:
    nc = Nextcloud(config_file=args.config, password=args.password)
    # Get the list of users from the Nextcloud server administration
    existing_nextcloud_users = get_user_ids(nc)
    # Get the list of users from the master user list in the Excel file
    master_user_list = load_users_from_spreadsheet(nc)

    for user_id in existing_nextcloud_users:
        if user_id == 'Admin':
            continue

        if user_id not in user_names:
            user = get_user(args, user_id)
            if not args.dry_run:
                logger.warning(f'Disabling user {user_id} not found in the master user list')
                user['ocs']['data']['enabled'] = False
                update_user(args, user['ocs']['data'])
            else:
                logger.info(f'Dry-run: Would have disabled user {user_id}')

    for record in records:
        if record['Mail'] not in user_ids:
            if not args.dry_run:
                logger.info(f'Adding user: {record['Mail']}')
                user = {
                    'userid': record['Mail'],
                    'password': generate_password(),
                    'displayName': record['Naam']
                }
                create_user(nc, user)
            else:
                logger.info(f'Dry-run: Would have added user {record['Mail']}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update users in the Nextcloud database')

    user_help = 'The username of the admin user'
    parser.add_argument('-u', '--username', type=str, help=user_help, required=True)

    password_help = 'The password of the admin user'
    parser.add_argument('-p', '--password', type=str, help=password_help, required=True)

    dry_run_help = 'Do not actually update the users'
    parser.add_argument('--dry-run', action='store_true', help=dry_run_help, default=True)

    args = parser.parse_args()
    main(args)