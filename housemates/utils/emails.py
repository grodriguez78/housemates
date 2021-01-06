# Standard Libraries
import base64
from datetime import datetime
import re


def get_bill_cost(email_data):

    # Check for message body
    if email_data['payload']['body']['size'] > 0:
        msg_raw = email_data['payload']

    # Use payload parts
    else:
        msg_raw = email_data['payload']['parts'][0]

    msg_bytes = base64.b64decode(msg_raw['body']['data'], '-_')
    msg = msg_bytes.decode('utf-8')

    # Search for monetary values in email
    match = re.search(r"\B[$]([0-9]+).([0-9]+)\b", msg)
    if match:
        cost_str = match.group()
        cost = float(cost_str.strip("$"))
    else:
        cost = None

    return cost


def get_received_date(email_data):
    received_date = datetime.fromtimestamp(int(email_data['internalDate']) / 1000)
    return received_date


def get_sender(email_data, aliases={}):

    sender_data = list(filter(lambda h: h['name'] == 'Return-Path', email_data['payload']['headers']))
    sender_domain = sender_data[0]['value'].split('.')[-2].split("@")[-1]

    # TODO: Improve alias handling to differentiate between Recology & SFPower (both use kubra)
    if sender_domain in aliases.keys():
        sender_name = aliases[sender_domain]
    else:
        sender_name = sender_domain

    return sender_name
