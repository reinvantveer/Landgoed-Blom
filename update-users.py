import argparse
import csv
from argparse import Namespace

import requests
from loguru import logger


def generate_password():
    pass



def main(args: Namespace):
    records: list[dict[str, str]] = []
    user_names: list[str] = []

    with open(args.file) as f:
        # Parse the CSV file
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
            user_names.append(row['Mail'])

    users = get_user_ids(args)

    user_ids = users['ocs']['data']['users']
    for user_id in user_ids:
        if user_id == 'Admin':
            continue

        if user_id not in user_names:
            user = get_user(args, user_id)
            if not args.dry_run:
                nc.users.disable(user.user_id)
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

def create_user(args: Namespace, user: dict) -> None:
    resp = requests.post(
        url=f'{args.server}/ocs/v1.php/cloud/users',
        json=user,
        auth=(args.username, args.password),
        headers={
            'OCS-APIRequest': 'true',
            'Content-Type': 'application/json'
        }
    )
    resp.raise_for_status()


def update_user(args: Namespace, user: dict) -> None:
    resp = requests.put(
        url=f'{args.server}/ocs/v1.php/cloud/users/{user["id"]}',
        json=user,
        auth=(args.username, args.password),
        headers={
            'OCS-APIRequest': 'true',
            'Content-Type': 'application/json'
        }
    )
    resp.raise_for_status()


def get_user(args, user_id) -> dict:
    resp = requests.get(
        url=f'{args.server}/ocs/v1.php/cloud/users/{user_id}?format=json',
        auth=(args.username, args.password),
        headers={'OCS-APIRequest': 'true'}
    )
    resp.raise_for_status()
    user = resp.json()
    return user


def get_user_ids(args):
    """Read out the users in Nextcloud"""
    resp = requests.get(
        url=f'{args.server}/ocs/v1.php/cloud/users?format=json',
        auth=(args.username, args.password),
        headers={'OCS-APIRequest': 'true'}
    )
    resp.raise_for_status()
    users = resp.json()

    return users


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