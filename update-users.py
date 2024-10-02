import argparse
import csv
from argparse import Namespace

from loguru import logger
from nc_py_api import Nextcloud


def main(args: Namespace):
    records: list[dict[str, str]] = []
    user_names: list[str] = []

    with open(args.file) as f:
        # Parse the CSV file
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
            user_names.append(row['Mail'])

    # Read out the users in Nextcloud
    nc = Nextcloud(nextcloud_url=args.server, username=args.username, password=args.password)
    users = []
    for user_id in nc.users.get_list():
        user = nc.users.get_user(user_id)
        users.append(user)

        if user.user_id not in user_names:
            logger.warning(f'Disabling user {user.user_id} not found in the master user list')
            if not args.dry_run:
                nc.users.disable(user.user_id)
            else:
                logger.info(f'Dry-run: Would have disabled user {user.user_id}')

    for record in records:
        logger.info(f'Updating user: {record['username']}')

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