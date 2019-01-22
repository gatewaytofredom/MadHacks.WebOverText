import yaml
from twilio.rest import Client

class smsSender:

    # load Twilio account info from configuration file
    with open("config.yaml", 'r') as stream:
        try:
            configuration = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = configuration['account_sid']
    auth_token = configuration['auth_token']

    client = Client(account_sid, auth_token)

    outbound_number = None

    def send(self,message,outbound_number):
        message = self.client.messages \
        .create(
            body=str(message),
            from_='+17155046198',
            to=outbound_number
        )