import argparse
import csv
from argparse import Namespace

from nc_py_api import Nextcloud


def main(args: Namespace):
    records: list[dict[str, str]] = []

    with open(args.file) as f:
        # Parse the CSV file
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    # Read out the users in Nextcloud
    nc = Nextcloud(nextcloud_url=args.server, username=args.username, password=args.password)
    users = []
    for user_id in nc.users.get_list():
        users.append(nc.users.get_user(user_id))

    for record in records:
        print(f"Updating user: {record['username']}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update users in the Nextcloud database')

    user_help = 'The username of the admin user'
    parser.add_argument('-u', 'username', type=str, help=user_help, required=True)

    admin_help = 'The password of the admin user'
    parser.add_argument('-p', 'password', type=str, help=admin_help, required=True)

    update_help = 'The file containing the users to update'
    csv_path = 'data/users.csv'
    parser.add_argument('-f', 'file', type=str, help=update_help, default=csv_path)

    server_help = 'The URL of the Nextcloud server'
    server_default = 'https://https://nx52347.your-storageshare.de/'
    parser.add_argument('-s', 'server', type=str, help=server_help, default=server_default)

    args = parser.parse_args()
    main(args)