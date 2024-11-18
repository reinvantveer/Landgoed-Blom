import smtplib
import ssl
import tomllib
from email.mime.text import MIMEText


class LandgoedBlomMailServer:
    def __init__(self, config_file: str) -> None:
        # Load the config file
        with open(config_file, 'rb') as f:
            self.config = tomllib.load(f)['tool']['landgoed-blom']

        # Load the email template
        with open('templates/create.md') as f:
            self.create_template = f.read()

        # Create the SSL context
        self.context = ssl.create_default_context()

        # Load the password from the environment
        self.config['smtp_password'] = os.environ['SMTP_PASSWORD']


    def send_create_mail(self, display_name: str, user_name: str, user_email: str, user_password: str) -> None:
        """
        Send the mail to the user with the login information

        Args:
            display_name: The display name of the user
            user_name: The name of the user
            user_email: The email address of the user
            user_password: The password of the user
        """

        with smtplib.SMTP_SSL(self.config['smtp_server'], self.config['smtp_port'], context=self.context) as server:
            server.login(self.config['smtp_username'], self.config['smtp_password'])

            mail_text = self.create_template.format(
                name=display_name,
                username=user_name,
                password=user_password
            )

            msg = MIMEText(mail_text, 'plain')
            msg['Subject'] = 'Welkom bij Landgoed Blom Nextcloud'
            msg['From'] = self.config['smtp_username']
            msg['To'] = user_email

            server.sendmail(self.config['smtp_username'], user_email, msg.as_string())

