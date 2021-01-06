# Module Libraries
from .utils import emails

class Bill():

    sender = None
    total = None
    recieved_date = None

    def __init__(self, sender, total, recieved_date):

        self.sender = sender
        self.total = total
        self.recieved_date = recieved_date

    @classmethod
    def from_email(cls, email_data, **kwargs):


        # Get Sender Name
        sender = emails.get_sender(email_data, **kwargs)

        # Get Total Bill Cost
        total = emails.get_bill_cost(email_data)

        # Get Date Bill was Received
        received_date = emails.get_received_date(email_data)

        bill = cls(sender, total, received_date)
        return bill

    def __repr__(self):
        return "Bill(sender={}, total={})".format(self.sender, self.total)

    def __str__(self):
        return "Bill of ${} from {}".format(self.total, self.sender)
