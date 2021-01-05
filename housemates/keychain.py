# Standard Libraries
import json
import os

class Keychain(object):
    # Store authentication secrets

    def __init__(self):
        self.keys = {}
        self.credentials = {}

        self._load_api_credentials()

    def _load_api_credentials(self):
        """ Load Application Credentials

        """

        # Get credentials directory
        root = os.path.dirname(os.path.dirname(__file__))
        creds_dir = root + "/.credentials"

        # Load all credentials
        for fn in os.listdir(creds_dir):
            app_name = fn.split(".")[0]
            with open(creds_dir + "/" + fn, 'r') as file:

                app_creds = json.load(file)
            self.credentials[app_name] = app_creds

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

        app_key = self.credentials[app]["consumer_key"]
        app_secret = self.credentials[app]["consumer_secret"]
        return app_key, app_secret
