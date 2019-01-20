"""Get monzo API details."""
import requests
import datetime

from monzo.monzo import Monzo
from monzo.auth import MonzoOAuth2Client

# Compensate for lately opened Monzo account
MONTHLY_SPEND_OFFSET = 600


class MonzoGetter:

    def __init__(self, access_token):
    # def __init__(self, access_token, client_id, client_secret, redirect_url):
        """Instantiate object with access token and account id."""
        self._access_token = access_token

        # oauth_client = MonzoOAuth2Client(
        #     client_id,
        #     client_secret,
        #     redirect_uri="http://127.0.0.1:21234"
        #     # redirect_uri=redirect_url
        # )

        # auth_start_url = oauth_client.authorize_token_url()
        # print(auth_start_url)
        # # Now user receives link.
        # # Code from link gets entered below
        # code = input("Enter code >>> ")
        # oauth_client.fetch_access_token(code)
        # self._client = Monzo.from_oauth_session(oauth_client)#

        self._client = Monzo(access_token)
        self._account_id = self._client.get_first_account()['id']


    def get_access_token(client_id):
        """Get authorization."""
        data = {
            'client_id': client_id,
            'redirect_uri': "http://127.0.0.1:21234",
            'response_type': 'code',
            'state': "afjalksjd2iwhfliuh24"
        }
        r = requests.post("http://auth.monzo.com", data=data)
        return r

    def get_balance(self):
        """Return JSON balance object."""
        return self._client.get_balance(self._account_id)

    def get_balance_pounds(self):
        return int(self.get_balance()['balance']) / 100

    def get_transactions(self):
        return self._client.get_transactions(self._account_id)['transactions']

    def get_monthly_spend_pounds(self):
        """Return money spent in last month."""
        today = datetime.datetime.today()
        month_start = datetime.datetime(today.year, today.month, 1)

        transactions = self.get_transactions()
        monthly_spend_pence = 0
        for transaction in transactions:
            date_str = transaction['created'][:10]
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            # If the transaction happened since the start of the month,
            # and it was a debit
            if date > month_start and transaction['amount'] < 0:
                monthly_spend_pence -= transaction['amount']

        return MONTHLY_SPEND_OFFSET + monthly_spend_pence / 100
