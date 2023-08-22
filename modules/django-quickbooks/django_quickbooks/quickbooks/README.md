# Quickbooks

By implementing this module, users will be able to process the accounting creation, payment processing, refund charges,
budget and payment management.

## Scope Features

The following are the critical features in scope of this module.

1. Secure and authorized Authentication.
2. Ability for account and attachments Management, including creation, retrieval, updating, and deletion.
3. Ability to manage bill payments.
4. Ability to manage Customer.
5. Ability to manage payments.
6. Ability to manage Invoices.

## Keys And Credentials Setup

Get the Quickbooks API keys and credentials by the following steps:

1. To get the quickbooks authorization code user have to visit
   the "https://developer.intuit.com/app/developer/playground"
2. Click on "Create New APP"
3. "Quickbook Online and Payments" then select "scopes" then click "create app" button.
4. After this "Development Settings" and "Production Settings" appear in the left sidebar, click on "Keys & Credentials"
   for either development or production, as needed.
5. Get you quickbooks client id and client secret and save it.
6. On the top right, click on profile icon and then go to the "Sandbox".
7. Copy your sandbox company id for your "INTUIT_QUICKBOOK_ACCOUNT_ID"
6. Assign it to the variable the name of the variable should be "INTUIT_QUICKBOOK_CLIENT_ID", "
   INTUIT_QUICKBOOK_CLIENT_SECRETS" and "INTUIT_QUICKBOOK_ACCOUNT_ID"

## Environment variables

```
INTUIT_QUICKBOOK_CLIENT_ID = ""
INTUIT_QUICKBOOK_CLIENT_SECRETS = ""
INTUIT_QUICKBOOK_ACCOUNT_ID = ""
```

## Api Table

List of api's endpoints with params needed for these apis.

| Api Name                                                                  |                                                                                                                             Param                                                                                                                              | Description                                                      |
|---------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:-----------------------------------------------------------------|
| `/modules/quickbook/access/token/`                                        |                                                                                                                  body_params `{"code" : ""}`                                                                                                                   | Takes authorization code and return access token.                |
| `/modules/quickbook/create-account/`                                      |                                                                                                                body_params `Name, AccountType`                                                                                                                 | Takes name and account type and create the account.              |
| `/modules/quickbook/read-account/<account_id>/`                           |                                                                                                                    path_params `account_id`                                                                                                                    | Takes account id and retrieve the detail.                        |
| `/modules/quickbook/update-account/`                                      |                                body_params  `Id, Name, FullyQualifiedName, domain, SubAccount, Description, Classification, AccountSubType , AccountType, SyncToken, CurrentBalanceWithSubAccounts,CurrentBalance and sparse `                                 | Takes update payload and update the account details.             |
| `/modules/quickbook/create-note-attachable/`                              |                                                                                 body_params  `{Note: "", AttachableRef:{IncludeOnSend: "" , EntityRef:{type:"", value:"" }}}`                                                                                  | Takes body params and return a created attachment.               |
| `/modules/quickbook/delete-attachable/`                                   |                                                                     body_params  `{SyncToken: "", Id:"", domain: "" , AttachableRef:{IncludeOnSend: "" , EntityRef:{type:"", value:"" }}}`                                                                     | Takes attachable id with other detail and delete the attachable. |
| `/modules/quickbook/retrieve-attachable/<attachable_id>/ `                |                                                                                                                  path_params  `attachable_id`                                                                                                                  | Takes attachable id and return the detail.                       |
| `/modules/quickbook/update-an-attachable/`                                |                                                                     body_params  `{SyncToken: "", Id:"", domain: "" , AttachableRef:{IncludeOnSend: "" , EntityRef:{type:"", value:"" }}}`                                                                     | This method returns a updated details of attachable.             |                                                                           |
| `/modules/quickbook/upload-an-attachable/`                                |                                                                                                                     form-data: `FileName`                                                                                                                      | This method used to upload the attachable.                       |                                                                           |
| `/modules/quickbook/create-bill-payment/`                                 |     body_params `{"PrivateNote": "", "domain": "","VendorRef": {"name": "", "value": ""}, "TotalAmt":  "PayType": "", "Line": [{"Amount": , "LinkedTxn": [{"TxnId": "", "TxnType": ""}]}], "CheckPayment": {"BankAccountRef": {"name": "", "value": ""}}}`     | This method used to create a bill payment.                       |                                                                           |
| `/modules/quickbook/void-bill-payment/`                                   |                                                                                                              body_params  `SyncToken, sparse, Id`                                                                                                              | This method is used to void the bill payment.                    |                                                                           |
| `/modules/quickbook/delete-bill-payment/`                                 |                                                                                                                  body_params  `SyncToken, Id`                                                                                                                  | This method used to delete the bill payment                      |                                                                           |
| `/modules/quickbook/retrieve-bill-payment/<bill_payment_id>/`             |                                                                                                                 path_params  `bill_payment_id`                                                                                                                 | This method is used to retrieve the bill payment.                |                                                                           |
| `/modules/quickbook/update-bill-payment/`                                 | body_params `{"PrivateNote": "", "domain": "", Id:"" ,"VendorRef": {"name": "", "value": ""}, "TotalAmt":  "PayType": "", "Line": [{"Amount": , "LinkedTxn": [{"TxnId": "", "TxnType": ""}]}], "CheckPayment": {"BankAccountRef": {"name": "", "value": ""}}}` | This method is used to update the bill payment.                  |                                                                           |
| `/modules/quickbook/create-payment/`                                      |                                                                                                 body_params  `{"TotalAmt": "", "CustomerRef": {"value": ""}}`                                                                                                  | This method is used to create the payment.                       |                                                                           |
| `/modules/quickbook/delete-payment/`                                      |                                                                                                                  body_params  `SyncToken, Id`                                                                                                                  | This method is used to delete the payment.                       |                                                                           |
| `/modules/quickbook/void-payment/`                                        |                                                                                                             body_params   `SyncToken, Id, sparse`                                                                                                              | This method is used to void the payment.                         |                                                                           |
| `/modules/quickbook/read-payment/<payment_id>/`                           |                                                                                                                   path_params  `payment_id`                                                                                                                    | This method is used to retrieve the payments.                    |                                                                           |
| `/modules/quickbook/send-payment/<payment_id>/send-to/<receiver_email>/ ` |                                                                                                    path_params  `payment_id`, query_params `receiver_email`                                                                                                    | This method is used to send the payments.                        |                                                                           |
| `/modules/quickbook/create-customer/`                                     |                                                                           body_params   `FullyQualifiedName, DisplayName, Notes, GivenName, Title, PrimaryEmailAddr, PrimaryPhone `                                                                            | This method is used to create the customer.                      |                                                                           |
| `/modules/quickbook/read-customer/<customer_id>/`                         |                                                                                                                   path_params  `customer_id`                                                                                                                   | This method is used to retrieve  the customer.                   |                                                                           |
| `/modules/quickbook/update-customer/`                                     |                                                                         body_params   `FullyQualifiedName, Id, DisplayName, Notes, GivenName, Title, PrimaryEmailAddr, PrimaryPhone `                                                                          | This method is used to update the customer.                      |                                                                           |
| `/modules/quickbook/create-invoice/`                                      |                                                                          body_params  `Line:{DetailType: "", Amount:"", SalesItemLineDetail:{ItemRef:"" }, CustomerRef:{value: ""}} `                                                                          | This method is used to create the invoice.                       |                                                                           |
| `/modules/quickbook/delete-invoice/`                                      |                                                                                                                  body_params  `SyncToken, Id`                                                                                                                  | This method is used to delete the invoice.                       |                                                                           |
| `/modules/quickbook/void-invoice/`                                        |                                                                                                                  body_params  `SyncToken, Id`                                                                                                                  | This method is used to void the invoice.                         |                                                                           |
| `/modules/quickbook/read-invoice/<invoice_id>/`                           |                                                                                                                   path_params  `invoice_id`                                                                                                                    | This method is used to retrieve the invoice.                     |                                                                           |
| `/modules/quickbook/send-invoice/<invoice_id>/`                           |                                                                                                    path_params  `invoice_id`, query_params `receiver_email                                                                                                     | This method is used to send the invoice.                         |                                                                           |
| `/modules/quickbook/update-invoice/`                                      |                                body_params  `{Id, DocNumber, SyncToken, domain, EmailStatus,sparse,ApplyTaxAfterDiscount,Balance,Line:{DetailType: "", Amount:"", SalesItemLineDetail:{ItemRef:"" }, CustomerRef:{value: ""}}}`                                | This method is used to retrieve the invoice.                     |                                                                           |

## Quickbooks Endpoints Postman Collection:

Here is a collection of all the api endpoints for the Quickbooks module.
[Quickbooks-Apis Postman Collection](https://drive.google.com/file/d/153erYVDW_uQFHzAyLBPLnMErGZsllSWV/view?usp=drive_link)

## Module Specifications

Here is
the [Module Specification Document](https://docs.google.com/document/d/1j4c0-YgRuZWh7sg66f5Y4zAHTbAlojzY2mspNPZbz58/edit?usp=sharing),
which provides more information about the module's actual intentions.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
