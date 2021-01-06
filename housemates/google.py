# Standard Libraries
import os.path
import pickle
import yaml

# Third Party Libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Module Libraries
from .bills import Bill


class GoogleHandler(object):

    creds_path = ".credentials/google_token.pickle"
    secrets_path = ".credentials/google.json"
    clients = {}
    api_versions = {
        'gmail': 'v1'
    }
    config = {}



    def __init__(self):

        # Get credentials (if they exist)
        self.creds = None
        if os.path.exists(self.creds_path):
            with open(self.creds_path, 'rb') as token:
                self.creds = pickle.load(token)

        # Load saved config
        config_fn = os.path.dirname(os.path.dirname(__file__)) + "/configs/google_config.yaml"
        with open(config_fn, 'r') as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)

        return

    def authenticate(self, apps):
        """ Authenticate with the Google API (if necessary)

        Valid Scopes:
            - gmail

        Parameters
        ---------
        apps : dict<string : string>
            Mapping of google service name to access type
        """

        #
        if apps is None:
            return

        # Construct Scopes list
        scopes = []
        scope_base = "https://www.googleapis.com/auth/{app}.{access}"
        for app, access in apps.items():
            scopes.append(scope_base.format(app=app, access=access))


        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(secrets_path, scopes)
                self.creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(self.creds_path, 'wb') as token:
                pickle.dump(self.creds, token)

        # Build new clients
        for app in apps.keys():
            self.clients[app] = build(app, self.api_versions[app], credentials=self.creds)

        return


    def scan_emails(self):
        """ Look for new bills in Gmail

        Return
        ------
        bills : TBD
            All unprocessed bills in Gmail

        """

        # Check that Gmail client has been instantiated
        if 'gmail' not in self.clients.keys():
            raise RuntimeError("Gmail API has not been authenticated!")

        client = self.clients['gmail']

        # Get Labe IDs used to denote unpaid Bills
        all_labels = client.users().labels().list(userId='me').execute()['labels']
        bill_labels = list(filter(lambda l: l['name'] in self.config['filter_label_names'], all_labels))
        bill_labelids = [l['id'] for l in bill_labels]

        # Get Bill Messages
        bill_msgs = client.users().messages().list(userId='me', labelIds=bill_labelids).execute()['messages']
        bill_msg_ids = [b['id'] for b in bill_msgs]

        bills = []
        for bill_id in bill_msg_ids:
            email_data = client.users().messages().get(userId='me', id=bill_id).execute()
            bills.append(Bill.from_email(email_data, aliases=self.config["sender_aliases"]))

        return bills
