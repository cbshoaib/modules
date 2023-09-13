from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .serializers import *


class QuickBooksTestCases(APITestCase):

    def setUp(self):
        self.headers = {
            "Quickbooks-Authorization": "uQmEDWWYQxAWWYQxATzkJScfVAuQmEDWWYQxATzkJScfkykfkykJScfkyk-uQmEDWWYQzkJfVAuQmEDWWYQxATzkJScfkykScfkykJScfkyk2"}

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.get_auth_token')
    def test_get_auth_token(self, get_auth_token_mock):
        mock_response = {'data': {
            "access_token": "uQmEDWWYQxAWWYQxATzkJScfVAuQmEDWWYQxATzkJScfkykfkykJScfkyk-uQmEDWWYQzkJfVAuQmEDWWYQxATzkJScfkykScfkykJScfkyk2",
            "token_type": "bearer",
            "x_refresh_token_expires_in": 87400,
            "id_token": "QmEDWWYQzkJfVAuQmEDWWYQxATzkJScfkykScfkykJScfkyk2-uQmEDWWYQxAWWYQxATzkJScfkykJScfkyk-uQmEDWWYQ0Zqe1dAD_7rd2_Lh-P_vPs6IqzsUYNc",
            "refresh_token": "mI4qlc7wIzJaQ66fHndkZY5uF9BGchz-QmEDWWYQzkJfVAuQmEDWWYQxATzkJScfkykScfkykJScfkyk2",
            "expires_in": 3800
        }}
        get_auth_token_mock.return_value = mock_response
        url = reverse('quickbook_service-create-access-token')
        data = {
            "code": "8BP4vbmI4qlc7wIzahdgbhw7dw7"
        }
        serializer = AccessTokenSerializer(data=data)
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['access_token'], mock_response['data']['access_token'])
        get_auth_token_mock.assert_called_once()

    def test_get_auth_token_without_authorization_code(self):
        url = reverse('quickbook_service-create-access-token')
        data = {
            "wrong_code": "8BP4vbmI4qlc7wIsSahd13gbhw7dw7"
        }
        serializer = AccessTokenSerializer(data=data)
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.create_account')
    def test_create_account(self, create_account_mock):
        mock_response = {'data': {
            "Account": {
                "Name": "test_account",
                "FullyQualifiedName": "new_account",
                "Active": "true",
                "Classification": "ability",
                "AccountType": "Accounts Payable",
                "AccountSubType": "AccountsPayable",
                "CurrentBalance": 0,
                "CurrentBalanceWithSubAccounts": 0,
                "Id": "20",
                "SyncToken": "0",
                "MetaData": {
                    "CreateTime": "2023-08-23T04:10:16-07:00",
                    "LastUpdatedTime": "2023-08-23T04:10:16-07:00"
                }
            },
            "time": "2023-08-23T04:10:16.688-07:00"
        }}
        create_account_mock.return_value = mock_response
        url = reverse('quickbook_service-create-an-account')
        data = {
            "Name": "cb_demo_test",
            "AccountType": "Accounts Payable"
        }
        serializer = CreateAccountSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Account'], mock_response['data']['Account'])
        create_account_mock.assert_called_once()

    def test_create_account_with_invalid_data(self):
        url = reverse('quickbook_service-create-an-account')
        data = {
            "name": "cb_demo_test",
            "account_type": "Accounts Payable"
        }
        serializer = CreateAccountSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.read_account')
    def test_read_account(self, read_account_mock):
        mock_response = {'data': {
            "Account": {
                "Name": "test_account",
                "FullyQualifiedName": "new_account",
                "Active": "true",
                "Classification": "ability",
                "AccountType": "Accounts Payable",
                "AccountSubType": "AccountsPayable",
                "CurrentBalance": 0,
                "CurrentBalanceWithSubAccounts": 0,
                "CurrencyRef": {
                    "value": "USD",
                    "name": "United States Dollar"
                },
                "Id": "20",
                "SyncToken": "0",
                "MetaData": {
                    "CreateTime": "2023-08-23T04:10:16-07:00",
                    "LastUpdatedTime": "2023-08-23T04:10:16-07:00"
                }
            },
            "time": "2023-08-23T04:10:16.688-07:00"
        }}
        read_account_mock.return_value = mock_response
        url = reverse('quickbook_service-read-an-account', kwargs={'account_id': 20})
        response = self.client.get(url, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Account']['Id'], mock_response['data']['Account']['Id'])
        read_account_mock.assert_called_once()

    def test_read_account_with_invalid_id(self):
        url = reverse('quickbook_service-read-an-account', kwargs={'account_id': 20})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['fault']['type'], 'AUTHENTICATION')

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.full_update_account')
    def test_full_update_account(self, full_update_account_mock):
        mock_response = {'data': {
            "Account": {
                "Name": "demo_account",
                "FullyQualifiedName": "demo_account",
                "Active": "true",
                "Classification": "ability",
                "CurrentBalance": 0,
                "CurrentBalanceWithSubAccounts": 0,
                "CurrencyRef": {
                    "value": "USD",
                    "name": "United States Dollar"
                },
                "Id": "20",
                "SyncToken": "1",
                "MetaData": {
                    "CreateTime": "2023-08-23T04:10:16-07:00",
                    "LastUpdatedTime": "2023-08-23T04:10:16-07:00"
                }
            },
            "time": "2023-08-23T04:10:16.688-07:00"
        }}
        full_update_account_mock.return_value = mock_response
        url = reverse('quickbook_service-update-full-account-detail')
        data = {
            "Description": "Description added during update.",
            "Classification": "Liability",
            "AccountSubType": "AccountsPayable",
            "CurrentBalanceWithSubAccounts": -1091.23,
            "AccountType": "Accounts Payable",
            "CurrentBalance": -1091.23,
            "SyncToken": "0",
            "Id": "20",
            "Name": "test_demo"
        }
        serializer = UpdateAccountSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Account']['Id'], mock_response['data']['Account']['Id'])
        full_update_account_mock.assert_called_once()

    def test_full_update_account_with_invalid_data(self):
        url = reverse('quickbook_service-update-full-account-detail')
        data = {
            "Description": "Description added during update.",
            "Classification": "Liability",
            "AccountSubType": "AccountsPayable",
            "CurrentBalanceWithSubAccounts": -1091.23,
            "AccountType": "Accounts Payable",
            "CurrentBalance": -1091.23,
            "SyncToken": "0",
            "Name": "test_demo"
        }
        serializer = UpdateAccountSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.create_note_attachable')
    def test_create_note_attachable(self, create_note_attachable_mock):
        mock_response = {'data': {
            "Attachable": {
                "Note": "This is new note.",
                "domain": "QBO",
                "Id": "855000001000",
                "SyncToken": "0",
                "MetaData": {
                    "CreateTime": "2023-08-23T04:52:56-07:00",
                    "LastUpdatedTime": "2023-08-23T04:52:56-07:00"
                },
                "AttachableRef": [
                    {
                        "EntityRef": {
                            "value": "20",
                            "type": "Invoice"
                        },
                    }
                ]
            },
            "time": "2023-08-23T04:52:56.064-07:00"
        }}
        create_note_attachable_mock.return_value = mock_response
        url = reverse('quickbook_service-create-a-note-attachable')
        data = {
            "Note": "This is a new note.",
            "AttachableRef": [
                {
                    "IncludeOnSend": "false",
                    "EntityRef": {
                        "type": "Invoice",
                        "value": "20"
                    }
                }
            ]
        }
        serializer = CreateNoteAttachableSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Attachable']['Note'], mock_response['data']['Attachable']['Note'])
        create_note_attachable_mock.assert_called_once()

    def test_create_note_attachable_with_invalid_data(self):
        url = reverse('quickbook_service-create-a-note-attachable')
        data = {
            "AttachableRef": [
                {
                    "IncludeOnSend": "false",
                    "EntityRef": {
                        "type": "Invoice",
                        "value": "20"
                    }
                }
            ]
        }
        serializer = CreateNoteAttachableSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.delete_attachable')
    def test_delete_attachable(self, delete_attachable_mock):
        mock_response = {'data': {
            "Attachable": {
                "domain": "QBO",
                "status": "Deleted",
                "Id": "54738633001"
            },
            "time": "2023-08-23T04:59:10.746-07:00"
        }}
        delete_attachable_mock.return_value = mock_response
        url = reverse('quickbook_service-delete-an-attachable')
        data = {
            "SyncToken": "0",
            "domain": "QBO",
            "AttachableRef": [
                {
                    "EntityRef": {
                        "type": "Invoice",
                        "value": "20"
                    }
                }
            ],
            "Id": "54738633001"
        }
        serializer = DeleteAttachableSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Attachable']['Id'], mock_response['data']['Attachable']['Id'])
        delete_attachable_mock.assert_called_once()

    def test_delete_attachable_with_invalid_data(self):
        url = reverse('quickbook_service-delete-an-attachable')
        data = {
            "SyncToken": "0",
            "domain": "QBO",
            "AttachableRef": [
                {
                    "EntityRef": {
                        "type": "Invoice",
                        "value": "20"
                    }
                }
            ],
        }
        serializer = DeleteAttachableSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.read_attachable')
    def test_read_attachable(self, read_attachable_mock):
        mock_response = {'data': {
            "Attachable": {
                "Note": "This is new note.",
                "domain": "QWO",
                "Id": "54738633001",
                "SyncToken": "0",
                "AttachableRef": [
                    {
                        "EntityRef": {
                            "value": "20",
                            "type": "Invoice"
                        },
                    }
                ]
            },
            "time": "2023-08-23T05:07:32.750-07:00"
        }}
        read_attachable_mock.return_value = mock_response
        url = reverse('quickbook_service-retrieve-an-attachable', kwargs={'attachable_id': 54738633001})
        response = self.client.get(url, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Attachable']['Id'], mock_response['data']['Attachable']['Id'])
        read_attachable_mock.assert_called_once()

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.update_attachable')
    def test_update_attachable(self, update_attachable_mock):
        mock_response = {'data': {
            "Attachable": {
                "Note": "Files note.",
                "domain": "QWE",
                "Id": "54738633001",
                "SyncToken": "0",
                "AttachableRef": [
                    {
                        "EntityRef": {
                            "value": "20",
                            "type": "Invoice"
                        },
                    }
                ]
            },
            "time": "2023-08-23T05:15:28.948-07:00"
        }}
        update_attachable_mock.return_value = mock_response
        url = reverse('quickbook_service-update-an-attachable')
        data = {
            "Note": "Files note.",
            "Id": "54738633001",
            "domain": "QWE",
            "SyncToken": "0",
            "AttachableRef": [
                {
                    "IncludeOnSend": "false",
                    "EntityRef": {
                        "type": "Invoice",
                        "value": "20"
                    }
                }
            ]
        }
        serializer = UpdateAttachableSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Attachable']['Id'], mock_response['data']['Attachable']['Id'])
        update_attachable_mock.assert_called_once()

    def test_update_attachable_with_invalid_data(self):
        url = reverse('quickbook_service-update-an-attachable')
        data = {
            "Note": "Files note.",
            "domain": "QWE",
            "SyncToken": "0",
            "AttachableRef": [
                {
                    "IncludeOnSend": "false",
                    "EntityRef": {
                        "type": "Invoice",
                        "value": "20"
                    }
                }
            ]
        }
        serializer = UpdateAttachableSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.create_a_bill_payment')
    def test_create_a_bill_payment(self, create_a_bill_payment_mock):
        mock_response = {'data': {
            "BillPayment": {
                "SyncToken": "0",
                "domain": "QBO",
                "VendorRef": {
                    "name": "bbbb",
                    "value": "20"
                },
                "TxnDate": "2015-07-14",
                "TotalAmt": 200.0,
                "PayType": "Check",
                "PrivateNote": "Acct.123",
                "Line": [
                    {
                        "Amount": 200.0,
                        "LinkedTxn": [
                            {
                                "TxnId": "123",
                                "TxnType": "Bill"
                            }
                        ]
                    }
                ],
                "Id": "20",
                "CheckPayment": {
                    "PrintStatus": "NeedToPrint",
                    "BankAccountRef": {
                        "name": "Checking",
                        "value": "20"
                    }
                },
            },
            "time": "2015-07-14T12:34:03.964-07:00"
        }}
        create_a_bill_payment_mock.return_value = mock_response
        url = reverse('quickbook_service-create-bill-payment')
        data = {
            "domain": "QBO",
            "VendorRef": {"name": "bbbb",
                          "value": "20"
                          },
            "TotalAmt": 10,
            "PayType": "Check",
            "Line": [
                {
                    "Amount": 0,
                    "LinkedTxn":
                        [
                            {
                                "TxnId": "234",
                                "TxnType": "Bill"}
                        ]}
            ],
            "CheckPayment":
                {
                    "BankAccountRef":
                        {
                            "name": "new_account",
                            "value": "96"
                        }
                }
        }
        serializer = CreateBillPaymentSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['BillPayment']['VendorRef'], mock_response['data']['BillPayment']['VendorRef'])
        create_a_bill_payment_mock.assert_called_once()

    def test_create_a_bill_payment_with_invalid_data(self):
        url = reverse('quickbook_service-create-bill-payment')
        data = {
            "VendorRef": {"name": "bbbb",
                          "value": "20"
                          },
            "TotalAmt": 10,
            "Line": [
                {
                    "Amount": 0,
                    "LinkedTxn":
                        [
                            {
                                "TxnId": "234",
                                "TxnType": "Bill"}
                        ]}
            ]
        }
        serializer = CreateBillPaymentSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.void_bill_payment')
    def test_void_bill_payment(self, void_bill_payment_mock):
        mock_response = {'data': {
            "BillPayment": {
                "VendorRef": {
                    "value": "20",
                    "name": "demo"
                },
                "PayType": "Check",
                "CheckPayment": {
                    "BankAccountRef": {
                        "value": "20",
                        "name": "demo"
                    },
                    "PrintStatus": "NotSet"
                },
                "TotalAmt": 0,
                "domain": "QWE",
                "Id": "20",
                "SyncToken": "0",
                "DocNumber": "11",
                "TxnDate": "2023-07-19",
                "PrivateNote": "Voided - Voided - Voided",
                "Line": []
            },
            "time": "2023-08-23T06:12:29.968-07:00"
        }}
        void_bill_payment_mock.return_value = mock_response
        url = reverse('quickbook_service-void-bill-payment')
        data = {
            "SyncToken": "0",
            "Id": "20",
            "sparse": True
        }
        serializer = VoidBillPaymentSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['BillPayment']['VendorRef'], mock_response['data']['BillPayment']['VendorRef'])
        void_bill_payment_mock.assert_called_once()

    def test_void_bill_payment_with_invalid_data(self):
        url = reverse('quickbook_service-void-bill-payment')
        data = {
            "SyncToken": "0",
            "sparse": True
        }
        serializer = VoidBillPaymentSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.delete_bill_payment')
    def test_delete_bill_payment(self, delete_bill_payment_mock):
        mock_response = {'data': {
            "BillPayment": {
                "status": "Deleted",
                "domain": "QWE",
                "Id": "20"
            },
            "time": "2015-05-26T13:17:25.316-07:00"
        }
        }
        delete_bill_payment_mock.return_value = mock_response
        url = reverse('quickbook_service-delete-bill-payment')
        data = {
            "SyncToken": "0",
            "Id": "20"
        }
        serializer = DeleteBillPaymentSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['BillPayment']['status'], mock_response['data']['BillPayment']['status'])
        delete_bill_payment_mock.assert_called_once()

    def test_delete_bill_payment_with_invalid_id(self):
        url = reverse('quickbook_service-delete-bill-payment')
        data = {
            "SyncToken": "0"
        }
        serializer = DeleteBillPaymentSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.read_bill_payment')
    def test_read_bill_payment(self, read_bill_payment_mock):
        mock_response = {'data': {
            "BillPayment": {
                "SyncToken": "0",
                "domain": "QBO",
                "VendorRef": {
                    "name": "bbbb",
                    "value": "20"
                },
                "TxnDate": "2015-07-14",
                "TotalAmt": 200.0,
                "PayType": "Check",
                "PrivateNote": "Acct.123",
                "Line": [
                    {
                        "Amount": 200.0,
                        "LinkedTxn": [
                            {
                                "TxnId": "123",
                                "TxnType": "Bill"
                            }
                        ]
                    }
                ],
                "Id": "20",
                "CheckPayment": {
                    "PrintStatus": "NeedToPrint",
                    "BankAccountRef": {
                        "name": "Checking",
                        "value": "20"
                    }
                },
            },
            "time": "2015-07-14T12:34:03.964-07:00"
        }}
        read_bill_payment_mock.return_value = mock_response
        url = reverse('quickbook_service-retrieve-an-bill-payment', kwargs={"bill_payment_id": 20})
        response = self.client.get(url, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['BillPayment']['Id'], mock_response['data']['BillPayment']['Id'])
        read_bill_payment_mock.assert_called_once()

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.update_a_bill_payment')
    def test_update_a_bill_payment(self, update_a_bill_payment_mock):
        mock_response = {'data': {
            "BillPayment": {
                "SyncToken": "0",
                "domain": "QBO",
                "VendorRef": {
                    "name": "bbbb",
                    "value": "20"
                },
                "TxnDate": "2015-07-14",
                "TotalAmt": 100.0,
                "PayType": "Check",
                "PrivateNote": "Acct.123",
                "Line": [
                    {
                        "Amount": 100.0,
                        "LinkedTxn": [
                            {
                                "TxnId": "123",
                                "TxnType": "Bill"
                            }
                        ]
                    }
                ],
                "Id": "20",
                "CheckPayment": {
                    "PrintStatus": "NeedToPrint",
                    "BankAccountRef": {
                        "name": "Checking",
                        "value": "20"
                    }
                },
                "MetaData": {
                    "CreateTime": "2015-07-14T12:34:04-07:00",
                    "LastUpdatedTime": "2015-07-14T12:34:04-07:00"
                }
            },
            "time": "2015-07-14T12:34:03.964-07:00"
        }}
        update_a_bill_payment_mock.return_value = mock_response
        url = reverse('quickbook_service-update-bill-payment')
        data = {
            "SyncToken": "0",
            "domain": "QBO",
            "VendorRef": {
                "name": "bbbb",
                "value": "20"
            },
            "TxnDate": "2015-07-14",
            "TotalAmt": 100.0,
            "PayType": "Check",
            "PrivateNote": "A new private note",
            "Line": [
                {
                    "Amount": 100.0,
                    "LinkedTxn": [
                        {
                            "TxnId": "123",
                            "TxnType": "Bill"
                        }
                    ]
                }
            ],
            "Id": "20",
            "CheckPayment": {
                "BankAccountRef": {
                    "name": "Checking",
                    "value": "20"
                }
            }

        }
        serializer = UpdateBillPaymentSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['BillPayment']['Id'], mock_response['data']['BillPayment']['Id'])
        update_a_bill_payment_mock.assert_called_once()

    def test_update_a_bill_payment_with_invalid_data(self):
        url = reverse('quickbook_service-update-bill-payment')
        data = {
            "VendorRef": {
                "name": "bbbb",
                "value": "20"
            },
            "Line": [
                {
                    "LinkedTxn": [
                        {
                            "TxnId": "123",
                            "TxnType": "Bill"
                        }
                    ]
                }
            ],
        }
        serializer = UpdateBillPaymentSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.create_payment')
    def test_create_payment(self, create_payment_mock):
        mock_response = {'data': {
            "Payment": {
                "CustomerRef": {
                    "value": "20",
                    "name": "Test Module"
                },
                "DepositToAccountRef": {
                    "value": "4"
                },
                "TotalAmt": 30.0,
                "UnappliedAmt": 30.0,
                "domain": "QBO",
                "Id": "20",
                "SyncToken": "0",
                "MetaData": {
                    "CreateTime": "2023-08-23T06:49:06-07:00",
                    "LastUpdatedTime": "2023-08-23T06:49:06-07:00"
                },
                "TxnDate": "2023-08-23",
                "CurrencyRef": {
                    "value": "USD",
                    "name": "United States Dollar"
                },
                "Line": []
            },
            "time": "2023-08-23T06:49:05.992-07:00"
        }}
        create_payment_mock.return_value = mock_response
        url = reverse('quickbook_service-create-payment')
        data = {"TotalAmt": 30.0, "CustomerRef": {"value": "20"}}
        serializer = PaymentSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Payment']['TotalAmt'], mock_response['data']['Payment']['TotalAmt'])
        create_payment_mock.assert_called_once()

    def test_create_payment_with_invalid_amount(self):
        url = reverse('quickbook_service-create-payment')
        data = {"CustomerRef": {"value": "20"}}
        serializer = PaymentSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.delete_payment')
    def test_delete_payment(self, delete_payment_mock):
        mock_response = {'data': {
            "Payment": {
                "status": "Deleted",
                "domain": "QBO",
                "Id": "73"
            },
            "time": "2013-03-14T11:57:42.849-07:00"
        }}
        delete_payment_mock.return_value = mock_response
        url = reverse('quickbook_service-delete-payment')
        data = {
            "SyncToken": "0",
            "Id": "20"
        }
        serializer = DeletePaymentSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Payment']['status'], mock_response['data']['Payment']['status'])
        delete_payment_mock.assert_called_once()

    def test_delete_payment_with_invalid_id(self):
        url = reverse('quickbook_service-delete-payment')
        data = {
            "SyncToken": "0",
        }
        serializer = DeletePaymentSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.void_payment')
    def test_void_payment(self, void_payment_mock):
        mock_response = {'data': {
            "Payment": {
                "CustomerRef": {
                    "value": "9",
                    "name": "demo"
                },
                "DepositToAccountRef": {
                    "value": "20"
                },
                "TotalAmt": 0,
                "UnappliedAmt": 0,
                "domain": "QWE",
                "Id": "20",
                "SyncToken": "0",
                "TxnDate": "2023-07-24",
                "PrivateNote": "Voided",
                "Line": []
            },
            "time": "2023-08-23T07:01:49.378-07:00"
        }}
        void_payment_mock.return_value = mock_response
        url = reverse('quickbook_service-void-payment')
        data = {
            "SyncToken": "0",
            "Id": "20",
            "sparse": True
        }
        serializer = VoidPaymentSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Payment']['Id'], mock_response['data']['Payment']['Id'])
        void_payment_mock.assert_called_once()

    def test_void_payment_with_invalid_id(self):
        url = reverse('quickbook_service-void-payment')
        data = {
            "SyncToken": "0",
            "sparse": True
        }
        serializer = VoidPaymentSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.read_payment')
    def test_read_payment(self, read_payment_mock):
        mock_response = {'data': {
            "Payment": {
                "CustomerRef": {
                    "value": "9",
                    "name": "demo"
                },
                "DepositToAccountRef": {
                    "value": "20"
                },
                "PaymentMethodRef": {
                    "value": "2"
                },
                "TotalAmt": 0,
                "UnappliedAmt": 0,
                "domain": "QWE",
                "Id": "20",
                "SyncToken": "0",
                "TxnDate": "2023-07-24",
                "PrivateNote": "Voided",
                "Line": []
            },
            "time": "2023-08-23T07:01:49.378-07:00"
        }}
        read_payment_mock.return_value = mock_response
        url = reverse('quickbook_service-read-payment', kwargs={"payment_id": 20})
        response = self.client.get(url, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Payment']['Id'], mock_response['data']['Payment']['Id'])
        read_payment_mock.assert_called_once()

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.send_payment')
    def test_send_payment(self, send_payment_mock):
        mock_response = {'data': {
            "Payment": {
                "CustomerRef": {
                    "value": "20",
                    "name": "Test Module"
                },
                "DepositToAccountRef": {
                    "value": "4"
                },
                "TotalAmt": 30.0,
                "UnappliedAmt": 0,
                "domain": "QWE",
                "Id": "123",
                "SyncToken": "0",
                "TxnDate": "2023-08-22",
                "CurrencyRef": {
                    "value": "USD",
                    "name": "United States Dollar"
                },
                "Line": [
                    {
                        "Amount": 30.0,
                        "LinkedTxn": [
                            {
                                "TxnId": "123",
                                "TxnType": "Invoice"
                            }
                        ],
                        "LineEx": {}
                    }
                ]
            },
            "time": "2023-08-23T07:17:09.225-07:00"
        }}
        send_payment_mock.return_value = mock_response
        url = reverse('quickbook_service-send-payment', kwargs={"payment_id": 123})
        params = {
            "receiver_email": "demo.123@email.com"
        }
        response = self.client.post(url, headers=self.headers, params=params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Payment']['Id'], mock_response['data']['Payment']['Id'])
        send_payment_mock.assert_called_once()

    def test_send_payment_with_invalid_token(self):
        url = reverse('quickbook_service-send-payment', kwargs={"payment_id": 123})
        params = {
            "receiver_email": "demo.123@email.com"
        }
        response = self.client.post(url, params=params, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.create_customer')
    def test_create_customer(self, create_customer_mock):
        mock_response = {'data': {
            "Customer": {
                "Notes": "Here are other details.",
                "Balance": 0,
                "BalanceWithJobs": 0,
                "PreferredDeliveryMethod": "Print",
                "Id": "20",
                "SyncToken": "0",
                "GivenName": "test",
                "PrimaryPhone": {
                    "FreeFormNumber": "(111) 222-3333"
                },
                "PrimaryEmailAddr": {
                    "Address": "test@myemail.com"
                },
                "DefaultTaxCodeRef": {
                    "value": "2"
                }
            },
            "time": "2023-08-23T07:35:37.548-07:00"
        }}
        create_customer_mock.return_value = mock_response
        url = reverse('quickbook_service-create-customer')
        data = {
            "FullyQualifiedName": "cb test",
            "PrimaryEmailAddr": {
                "Address": "test@myemail.com"
            },
            "DisplayName": "Test customer",
            "Title": "Mr",
            "Notes": "Here are other details.",
            "PrimaryPhone": {
                "FreeFormNumber": "(111) 222-3333"
            },
            "BillAddr": {
                "CountrySubDivisionCode": "CA",
                "City": "Mountain View",
                "PostalCode": "12345",
                "Line1": "123 Main Street",
                "Country": "USA"
            },
            "GivenName": "test"
        }
        serializer = CustomerSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Customer']['Id'], mock_response['data']['Customer']['Id'])
        create_customer_mock.assert_called_once()

    def test_create_customer_with_invalid_data(self):
        url = reverse('quickbook_service-create-customer')
        data = {
            "PrimaryEmailAddr": {
                "Address": "test@myemail.com"
            },
            "PrimaryPhone": {
                "FreeFormNumber": "(111) 222-3333"
            },
            "BillAddr": {
                "CountrySubDivisionCode": "CA",
                "City": "Mountain View",
                "PostalCode": "12345",
                "Line1": "123 Main Street",
                "Country": "USA"
            },
            "GivenName": "test"
        }
        serializer = CustomerSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.read_customer')
    def test_read_customer(self, read_customer_mock):
        mock_response = {'data': {
            "Customer": {
                "Notes": "Here are other details.",
                "Balance": 0,
                "BalanceWithJobs": 0,
                "PreferredDeliveryMethod": "Print",
                "Id": "20",
                "SyncToken": "0",
                "GivenName": "test",
                "PrimaryPhone": {
                    "FreeFormNumber": "(111) 222-3333"
                },
                "PrimaryEmailAddr": {
                    "Address": "test@myemail.com"
                },
                "DefaultTaxCodeRef": {
                    "value": "2"
                }
            },
            "time": "2023-08-23T07:35:37.548-07:00"
        }}
        read_customer_mock.return_value = mock_response
        url = reverse('quickbook_service-read-customer', kwargs={'customer_id': 20})
        response = self.client.get(url, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Customer']['Id'], mock_response['data']['Customer']['Id'])
        read_customer_mock.assert_called_once()

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.update_customer')
    def test_update_customer(self, update_customer_mock):
        mock_response = {'data': {
            "Customer": {
                "Notes": "Here are other details.",
                "Balance": 0,
                "BalanceWithJobs": 0,
                "PreferredDeliveryMethod": "Print",
                "Id": "20",
                "SyncToken": "0",
                "GivenName": "test",
                "PrimaryPhone": {
                    "FreeFormNumber": "(111) 222-3333"
                },
                "PrimaryEmailAddr": {
                    "Address": "test@myemail.com"
                },
                "DefaultTaxCodeRef": {
                    "value": "2"
                }
            },
            "time": "2023-08-23T07:35:37.548-07:00"
        }}
        update_customer_mock.return_value = mock_response
        url = reverse('quickbook_service-update-customer')
        data = {
            "domain": "QBO",
            "PrimaryEmailAddr": {
                "Address": "update@Intuit.com"
            },
            "DisplayName": "Update CB",
            "GivenName": "Bill",
            "FullyQualifiedName": "Update CB",
            "BalanceWithJobs": 85.0,
            "PrimaryPhone": {
                "FreeFormNumber": "(415) 444-6538"
            },
            "Balance": 85.0,
            "SyncToken": "0",
            "CompanyName": "Update CB Shop",
            "Id": "20"
        }
        serializer = UpdateCustomerSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Customer']['Id'], mock_response['data']['Customer']['Id'])
        update_customer_mock.assert_called_once()

    def test_update_customer_with_invalid_id(self):
        url = reverse('quickbook_service-update-customer')
        data = {
            "PrimaryEmailAddr": {
                "Address": "update@Intuit.com"
            },
            "PrimaryPhone": {
                "FreeFormNumber": "(415) 444-6538"
            },
            "Balance": 85.0,
            "SyncToken": "0",
            "CompanyName": "Update CB Shop",
        }
        serializer = UpdateCustomerSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.create_invoice')
    def test_create_invoice(self, create_invoice_mock):
        mock_response = {'data': {
            "Invoice": {
                "domain": "QWE",
                "Id": "20",
                "SyncToken": "0",
                "DocNumber": "1056",
                "TxnDate": "2023-08-23",
                "LinkedTxn": [],
                "Line": [
                    {
                        "Id": "1",
                        "Amount": 10.0,
                        "DetailType": "SalesItemLineDetail",
                        "SalesItemLineDetail": {
                            "ItemRef": {
                                "value": "1",
                                "name": "Services"
                            },
                            "ItemAccountRef": {
                                "value": "1",
                                "name": "Services"
                            },
                            "TaxCodeRef": {
                                "value": "NON"
                            }
                        }
                    },
                    {
                        "Amount": 10.0,
                        "DetailType": "SubTotalLineDetail",
                        "SubTotalLineDetail": {}
                    }
                ],
                "DueDate": "2023-09-22",
                "TotalAmt": 10.0,
                "Balance": 10.0
            },
            "time": "2023-08-23T07:58:33.888-07:00"
        }}
        create_invoice_mock.return_value = mock_response
        url = reverse('quickbook_service-create-invoice')
        data = {
            "Line": [
                {
                    "DetailType": "SalesItems",
                    "Amount": 10.0,
                    "SalesItemLineDetail": {
                        "ItemRef": {
                            "name": "service",
                            "value": "1"
                        }
                    }
                }
            ],
            "CustomerRef": {
                "value": "20"
            }
        }
        serializer = CreateInvoiceSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Invoice']['Id'], mock_response['data']['Invoice']['Id'])
        create_invoice_mock.assert_called_once()

    def test_create_invoice_with_invalid_data(self):
        url = reverse('quickbook_service-create-invoice')
        data = {
            "Line": [
                {
                    "DetailType": "SalesItems",
                    "Amount": 10.0,
                    "SalesItemLineDetail": {
                        "ItemRef": {
                            "name": "service",
                            "value": "1"
                        }
                    }
                }
            ],
        }
        serializer = CreateInvoiceSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.delete_invoice')
    def test_delete_invoice(self, delete_invoice_mock):
        mock_response = {'data': {
            "Invoice": {
                "status": "Deleted",
                "domain": "QWE",
                "Id": "20"
            },
            "time": "2013-03-15T00:18:15.322-07:00"
        }}
        delete_invoice_mock.return_value = mock_response
        url = reverse('quickbook_service-delete-invoice')
        data = {
            "SyncToken": "0",
            "Id": "20"
        }
        serializer = DeleteInvoiceSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Invoice']['Id'], mock_response['data']['Invoice']['Id'])
        delete_invoice_mock.assert_called_once()

    def test_delete_invoice_with_invalid_id(self):
        url = reverse('quickbook_service-delete-invoice')
        data = {
            "SyncToken": "0",
        }
        serializer = CreateInvoiceSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.void_invoice')
    def test_void_invoice(self, void_invoice_mock):
        mock_response = {'data': {
            "Invoice": {
                "Id": "20",
                "SyncToken": "0",
                "CustomField": [
                    {
                        "DefinitionId": "0",
                        "Name": "new #",
                        "Type": "StringType"
                    }
                ],
                "DocNumber": "123",
                "TxnDate": "2023-08-23",
                "PrivateNote": "Voided",
                "LinkedTxn": [],
                "Line": [
                    {
                        "Id": "0",
                        "DetailType": "SalesItemLineDetail",
                        "SalesItemLineDetail": {
                            "ItemRef": {
                                "value": "1",
                                "name": "Services"
                            },
                            "ItemAccountRef": {
                                "value": "1",
                                "name": "Services"
                            },
                        }
                    },
                    {
                        "Amount": 0,
                        "DetailType": "SubTotalLineDetail",
                        "SubTotalLineDetail": {}
                    }
                ],
                "CustomerRef": {
                    "value": "59",
                    "name": "Demo Module"
                },
                "DueDate": "2023-09-22",
            },
            "time": "2023-08-23T08:10:12.393-07:00"
        }}
        void_invoice_mock.return_value = mock_response
        url = reverse('quickbook_service-void-invoice')
        data = {
            "SyncToken": "0",
            "Id": "20"
        }
        serializer = VoidInvoiceSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Invoice']['Id'], mock_response['data']['Invoice']['Id'])
        void_invoice_mock.assert_called_once()

    def test_void_invoice_with_invalid_id(self):
        url = reverse('quickbook_service-void-invoice')
        data = {
            "SyncToken": "0",
        }
        serializer = VoidInvoiceSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.read_invoice')
    def test_read_invoice(self, read_invoice_mock):
        mock_response = {'data': {
            "Invoice": {
                "Id": "20",
                "SyncToken": "0",
                "DocNumber": "123",
                "TxnDate": "2023-08-23",
                "CurrencyRef": {
                    "value": "USD",
                    "name": "United States Dollar"
                },
                "PrivateNote": "Voided",
                "LinkedTxn": [],
                "Line": [
                    {
                        "Id": "0",
                        "DetailType": "SalesItemLineDetail",
                        "SalesItemLineDetail": {
                            "ItemRef": {
                                "value": "1",
                                "name": "Services"
                            },
                            "ItemAccountRef": {
                                "value": "1",
                                "name": "Services"
                            },
                        }
                    },
                ],
                "CustomerRef": {
                    "value": "59",
                    "name": "Demo Module"
                },
                "DueDate": "2023-09-22",
            },
            "time": "2023-08-23T08:10:12.393-07:00"
        }}
        read_invoice_mock.return_value = mock_response
        url = reverse('quickbook_service-read-invoice', kwargs={'invoice_id': 20})
        response = self.client.get(url, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Invoice']['Id'], mock_response['data']['Invoice']['Id'])
        read_invoice_mock.assert_called_once()

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.send_invoice')
    def test_send_invoice(self, send_invoice_mock):
        mock_response = {'data': {
            "Invoice": {
                "InvoiceLink": "https://developer.intuit.com/comingSoonview",
                "domain": "QWE",
                "Id": "20",
                "SyncToken": "0",
                "CustomField": [
                    {
                        "DefinitionId": "1",
                        "Name": "new #",
                        "Type": "StringType"
                    }
                ],
                "DocNumber": "123",
                "TxnDate": "2023-08-23",
                "CurrencyRef": {
                    "value": "USD",
                    "name": "United States Dollar"
                },
                "PrivateNote": "Voided",
                "LinkedTxn": [],
                "Line": [
                    {
                        "Id": "1",
                        "LineNum": 1,
                        "Amount": 0,
                        "DetailType": "SalesItemLineDetail",
                        "SalesItemLineDetail": {
                            "ItemRef": {
                                "value": "1",
                                "name": "Services"
                            },
                        }
                    },
                ],
                "DueDate": "2023-09-22",
                "BillEmail": {
                    "Address": "demomodule.123@gmail.com"
                },
            },
            "time": "2023-08-23T08:21:29.199-07:00"
        }}
        send_invoice_mock.return_value = mock_response
        url = reverse('quickbook_service-send-invoice', kwargs={"invoice_id": 20})
        params = {
            "receiver_email": "demo.123@email.com"
        }
        response = self.client.post(url, headers=self.headers, params=params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Invoice']['Id'], mock_response['data']['Invoice']['Id'])
        send_invoice_mock.assert_called_once()

    def test_send_invoice_without_token(self):
        url = reverse('quickbook_service-send-invoice', kwargs={"invoice_id": 20})
        params = {
            "receiver_email": "demo.123@email.com"
        }
        response = self.client.post(url, params=params, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch('modules.django_quickbooks.quickbooks.services.quickbooks.QuickbooksService.update_invoice')
    def test_update_invoice(self, update_invoice_mock):
        mock_response = {'data': {
            "Invoice": {
                "domain": "QWE",
                "Id": "20",
                "SyncToken": "0",
                "DocNumber": "123",
                "TxnDate": "2023-08-23",
                "CurrencyRef": {
                    "value": "USD",
                    "name": "United States Dollar"
                },
                "LinkedTxn": [],
                "Line": [
                    {
                        "Id": "1",
                        "Amount": 10.0,
                        "DetailType": "SalesItemLineDetail",
                        "SalesItemLineDetail": {
                            "ItemRef": {
                                "value": "1",
                                "name": "Services"
                            },
                        }
                    },
                    {
                        "Amount": 10.0,
                        "DetailType": "SubTotalLineDetail",
                        "SubTotalLineDetail": {}
                    }
                ],
                "DueDate": "2023-09-22",
                "TotalAmt": 10.0,
                "Balance": 10.0
            },
            "time": "2023-08-23T07:58:33.888-07:00"
        }}
        update_invoice_mock.return_value = mock_response
        url = reverse('quickbook_service-update-invoice')
        data = {
            "DocNumber": "20",
            "SyncToken": "0",
            "domain": "QWE",
            "Balance": 10.0,
            "TxnDate": "2015-07-24",
            "TotalAmt": 10.0,
            "CustomerRef": {
                "name": "Amy's Bird Sanctuary",
                "value": "1"
            },
            "DueDate": "2023-09-22",
            "EmailStatus": "NotSet",
            "Line": [
                {
                    "DetailType": "SalesItemLineDetail",
                    "Amount": 100.0,
                    "SalesItemLineDetail": {
                        "ItemRef": {
                            "name": "Services",
                            "value": "1"
                        }
                    }
                }
            ],
            "Id": "20"

        }
        serializer = UpdateInvoiceSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Invoice']['Id'], mock_response['data']['Invoice']['Id'])
        update_invoice_mock.assert_called_once()

    def test_update_invoice_with_invalid_id(self):
        url = reverse('quickbook_service-update-invoice')
        data = {
            "CustomerRef": {
                "name": "Amy's Bird Sanctuary",
                "value": "1"
            },
            "DueDate": "2023-09-22",
            "EmailStatus": "NotSet",
            "Line": [
                {
                    "DetailType": "SalesItemLineDetail",
                    "Amount": 100.0,
                    "SalesItemLineDetail": {
                        "ItemRef": {
                            "name": "Services",
                            "value": "1"
                        }
                    }
                }
            ],
        }
        serializer = UpdateInvoiceSerializer(data=data)
        response = self.client.post(url, data=data, headers=self.headers, format='json')
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
