# Standard Libraries
import os

class Keychain(object):
    # Store authentication secrets

    def __init__(self):
        self.keys = {}
        self.credentials = {}

        self._load_api_credentials()


    def _load_api_credentials(self):
        """ Load Application Secrets from Environment

        """

        for var in ['SPLITWISE_CONSUMER_KEY', 'SPLITWISE_CONSUMER_SECRET']:
            if var not in os.environ.keys():
                raise RuntimeError("Mssing {} environment variable!".format(var))

        self.credentials["splitwise"] = {
            "key" : os.environ['SPLITWISE_CONSUMER_KEY'],
            "secret" : os.environ['SPLITWISE_CONSUMER_SECRET'],
        }
        return

    def add_secret(self, name, key):

        # Check for existing keys
        if name in self.keys.keys():
            raise ValueError("A secret for {} is already in the keychain!".format(name))

        # Add key to keychain
        self.keys[name] = key
        return

    def get_secret(self, name):

        secret = None
        if name in self.keys.keys():
            secret = self.keys[name]

        return secret

    def get_api_credentials(self, app):
        """ Access the API credentials for a specific application

        """

        app_key = self.credentials[app]["key"]
        app_secret = self.credentials[app]["secret"]
        return app_key, app_secret
