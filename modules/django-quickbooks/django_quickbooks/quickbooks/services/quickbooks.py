import base64
import json
import os

import requests
from rest_framework import status


class QuickbookBase:
    def __init__(self):
        self.INTUIT_QUICKBOOK_BASE_URL = os.getenv('INTUIT_QUICKBOOK_BASE_URL', "")
        self.INTUIT_QUICKBOOK_CLIENT_ID = os.getenv('INTUIT_QUICKBOOK_CLIENT_ID', "")
        self.INTUIT_QUICKBOOK_CLIENT_SECRETS = os.getenv('INTUIT_QUICKBOOK_CLIENT_SECRETS', "")
        self.INTUIT_QUICKBOOK_ACCOUNT_ID = os.getenv('INTUIT_QUICKBOOK_ACCOUNT_ID', "")

    @staticmethod
    def basic_auth(client_id, client_secret):
        """
        Find basic auth, and returns base64 encoded
        """
        credentials = "%s:%s" % (client_id, client_secret)
        return base64.b64encode(credentials.encode('utf-8')).decode('utf-8').replace("\n", "")

    def get_headers(self, access_token):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        return headers

    def _api_call(self, request_type, url, headers=None, payload=None, data=None, params=None):
        try:
            response = requests.request(request_type, url, headers=headers, json=payload, data=data, params=params)
            data = json.loads(response.text)
            return {"data": data, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"data": e.response.json(), "status_code": e.response.status_code}


class QuickbooksService(QuickbookBase):
    def get_auth_token(self, code):
        try:
            url = f'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer'

            basic_auth_token = self.basic_auth(client_id=self.INTUIT_QUICKBOOK_CLIENT_ID,
                                               client_secret=self.INTUIT_QUICKBOOK_CLIENT_SECRETS
                                               )
            headers = {
                'Authorization': f'Basic {basic_auth_token}',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }

            payload = {
                "grant_type": "authorization_code",
                "redirect_uri": "https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl",
                "code": code
            }

            response = requests.request('POST', url, headers=headers, data=payload)
            if response.status_code == 200:
                return {"data": response.json(), "status_code": status.HTTP_200_OK}
            return {"data": {"error": response.json()}, "status_code": status.HTTP_400_BAD_REQUEST}
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def create_account(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/account?minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def read_account(self, access_token, account_id):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/account/{account_id}?minorversion=65'
            response = self._api_call(request_type='GET', url=url, headers=self.get_headers(access_token=access_token))
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def full_update_account(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/account?minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def create_note_attachable(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/attachable?minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def delete_attachable(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/attachable?operation=delete&minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def read_attachable(self, access_token, attachable_id):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/attachable/{attachable_id}?minorversion=65'
            response = self._api_call(request_type='GET', url=url, headers=self.get_headers(access_token=access_token))
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def update_attachable(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/attachable?minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def create_a_bill_payment(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/billpayment?minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def void_bill_payment(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/billpayment?operation=update&include=void&minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def delete_bill_payment(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/billpayment?operation=delete&minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def read_bill_payment(self, access_token, bill_payment_id):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/billpayment/{bill_payment_id}?minorversion=65'
            response = self._api_call(request_type='GET', url=url, headers=self.get_headers(access_token=access_token))
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def update_a_bill_payment(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/billpayment?minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def create_payment(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/payment?minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def delete_payment(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/payment?operation=delete&minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def void_payment(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/payment?operation=update&include=void&minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def read_payment(self, access_token, payment_id):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/payment/{payment_id}?minorversion=65'
            response = self._api_call(request_type='GET', url=url, headers=self.get_headers(access_token=access_token))
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def send_payment(self, access_token, payment_id, receiver_email):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/payment/{payment_id}/send?sendTo={receiver_email}&minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token))
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def create_customer(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/customer?minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def read_customer(self, access_token, customer_id):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/customer/{customer_id}?minorversion=65'
            response = self._api_call(request_type='GET', url=url, headers=self.get_headers(access_token=access_token))
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def update_customer(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/customer?minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def create_invoice(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/invoice?minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def delete_invoice(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/invoice?operation=delete&minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def void_invoice(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/invoice?operation=void&minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def read_invoice(self, access_token, invoice_id):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/invoice/{invoice_id}?minorversion=65'
            response = self._api_call(request_type='GET', url=url, headers=self.get_headers(access_token=access_token))
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def send_invoice(self, access_token, invoice_id, receiver_email):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/invoice/{invoice_id}/send?sendTo={receiver_email}&minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token))
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}

    def update_invoice(self, access_token, payload):
        try:
            url = f'{self.INTUIT_QUICKBOOK_BASE_URL}/v3/company/{self.INTUIT_QUICKBOOK_ACCOUNT_ID}/invoice?minorversion=65'
            response = self._api_call(request_type='POST', url=url, headers=self.get_headers(access_token=access_token),
                                      payload=payload)
            return response
        except Exception as e:
            return {"data": {"error": e.args}, "status_code": status.HTTP_400_BAD_REQUEST}
