import argparse
import csv
from argparse import Namespace

import requests
from loguru import logger


def main(args: Namespace):
    records: list[dict[str, str]] = []
    user_names: list[str] = []

    nc = Nextcloud(config_file=args.config, password=args.password)
    users = get_user_ids(nc)

    user_ids = users['ocs']['data']['users']
    for user_id in user_ids:
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
                create_user(args, user)
            else:
                logger.info(f'Dry-run: Would have added user {record['Mail']}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update users in the Nextcloud database')

    user_help = 'The username of the admin user'
    parser.add_argument('-u', '--username', type=str, help=user_help, required=True)

    password_help = 'The password of the admin user'
    parser.add_argument('-p', '--password', type=str, help=password_help, required=True)

    update_help = 'The file containing the users to update'
    csv_path = 'data/users.csv'
    parser.add_argument('-f', '--file', type=str, help=update_help, default=csv_path)

    server_help = 'The URL of the Nextcloud server'
    server_default = 'https://nx52347.your-storageshare.de/'
    parser.add_argument('-s', '--server', type=str, help=server_help, default=server_default)

    dry_run_help = 'Do not actually update the users'
    parser.add_argument('--dry-run', action='store_true', help=dry_run_help, default=True)

    args = parser.parse_args()
    main(args)