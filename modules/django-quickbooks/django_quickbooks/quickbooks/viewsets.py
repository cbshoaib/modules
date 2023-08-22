from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import *
from .services.quickbooks import QuickbookService


class QuickbookViewSet(viewsets.GenericViewSet):
    """
     QuickbookViewSet will take "QUICKBOOKS_AUTHORIZATION" to authenticate Quickbooks APIs and provide following functionality
    """
    allowed_serializers = {
        "create_access_token": AccessTokenSerializer,
        "create_an_account": CreateAccountSerializer,
        "update_full_account_detail": UpdateAccountSerializer,
        "create_a_note_attachable": CreateNoteAttachmentSerializer,
        "delete_an_attachable": DeleteAttachmentSerializer,
        "update_an_attachable": UpdateAttachmentSerializer,
        "upload_an_attachable": UploadAttachableSerializer,
        "create_bill_payment": CreateBillPaymentSerializer,
        "void_bill_payment": VoidBillPaymentSerializer,
        "delete_bill_payment": DeleteBillPaymentSerializer,
        "update_bill_payment": UpdateBillPaymentSerializer,
        "create_payment": PaymentSerializer,
        "delete_payment": DeletePaymentSerializer,
        "void_payment": VoidPaymentSerializer,
        "create_customer": CustomerSerializer,
        "update_customer": UpdateCustomerSerializer,
        "create_invoice": CreateInvoiceSerializer,
        "delete_invoice": DeleteInvoiceSerializer,
        "void_invoice": VoidInvoiceSerializer,
        "update_invoice": UpdateInvoiceSerializer
    }

    quickbook_service = QuickbookService()

    def get_serializer_class(self):
        return self.allowed_serializers.get(self.action)

    @action(detail=False, methods=['post'], url_path='access/token')
    def create_access_token(self, request):
        """
       Create Quickbooks access token to authenticate APIs
       :body_params str code: The code obtain from Quickbook API authorization link  \n
       :return: Access token with token details
       """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.get_auth_token(code=serializer.data['code'])
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='create-account')
    def create_an_account(self, request):
        """
        Create Quickbooks Account use to track transactions. \n
        :Quickbooks-Authorization: access_token (required)
        :body_params str Name: The name of account
        :body_params str AccountType: The name of account title
        :return: Account's details
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.create_account(access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
                                                         payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['get'], url_path='read-account/(?P<account_id>\d+)')
    def read_an_account(self, request, **kwargs):
        """
        Retrieve Quickbooks Account details. \n
        :Quickbooks-Authorization: access_token (required)
        :path_params str account_id: Create account id
        :return: Account's details
        """
        response = self.quickbook_service.read_account(access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
                                                       account_id=kwargs.get('account_id'))
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='update-account')
    def update_full_account_detail(self, request):
        """
        Update Quickbooks Account details. \n
        :Quickbooks-Authorization: access_token (required)
        :body_params:  Id, Name, FullyQualifiedName, domain, SubAccount, Description, Classification, AccountSubType
        AccountType, SyncToken, CurrentBalanceWithSubAccounts,CurrentBalance and sparse
        :return: Returns updated account's details
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.full_update_account(
            access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
            payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='create-note-attachable')
    def create_a_note_attachable(self, request):
        """
         Create a Note Attachable. \n
         :Quickbooks-Authorization: access_token (required)
         :body_params: Note,
         :body_params: AttachableRef:{IncludeOnSend, EntityRef}
         :body_params: EntityRef:{type, value}
         :return: Returns updated Attachable details
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.create_note_attachable(
            access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
            payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='delete-attachable')
    def delete_an_attachable(self, request):
        """
          Create a Note Attachable. \n
          :Quickbooks-Authorization: access_token (required)
          :body_params: SyncToken, Id, domain
          :body_params: AttachableRef:{IncludeOnSend, EntityRef}
          :body_params: EntityRef:{type, value}
          :return: Returns Deleted Attachable details.
         """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.delete_attachable(
            access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
            payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['get'], url_path='retrieve-attachable/(?P<attachable_id>\d+)')
    def retrieve_an_attachable(self, request, **kwargs):
        """
          Retrieve an Attachable details. \n
          :Quickbooks-Authorization: access_token (required)
          :path_params: attachable_id
          :return: Returns Attachable details.
         """
        response = self.quickbook_service.read_attachable(
            access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
            attachable_id=kwargs.get('attachable_id'))
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='update-an-attachable')
    def update_an_attachable(self, request):
        """
          Update a Note Attachable. \n
          :Quickbooks-Authorization: access_token (required)
          :body_params: SyncToken, Id, domain, Note
          :body_params: AttachableRef:{IncludeOnSend, EntityRef}
          :body_params: EntityRef:{type, value}
          :return: Returns details about updated Attachable.
         """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.update_attachable(
            access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
            payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='upload-an-attachable')
    def upload_an_attachable(self, request):
        """
          Upload an Attachable. \n
          :Quickbooks-Authorization: access_token (required)
          :body_params (form-data): FileName
          :return: Returns details about uploaded Attachable.
         """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.upload_attachable(
            access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
            payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='create-bill-payment')
    def create_bill_payment(self, request):
        """
        Create a bill payments. \n
        :Quickbooks-Authorization: access_token (required)
        :body_params: PrivateNote, TotalAmt, PayType, Note
        :body_params: VendorRef:{name, value}
        :body_params: Line:{Amount, LinkedTxn:{TxnId, TxnType}}
        :body_params: CheckPayment:{BankAccountRef:{name, value}}
        :return: Returns details about created bill payments.
       """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.create_a_bill_payment(
            access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
            payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='void-bill-payment')
    def void_bill_payment(self, request):
        """
         Void a bill payments. \n
         :Quickbooks-Authorization: access_token (required)
         :body_params: SyncToken, sparse, Id
         :return: Returns voided bill payments.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.void_bill_payment(
            access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
            payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='delete-bill-payment')
    def delete_bill_payment(self, request):
        """
        Delete a bill payments. \n
        :Quickbooks-Authorization: access_token (required)
        :body_params: SyncToken, Id
        :return: Returns deleted bill payments.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.delete_bill_payment(
            access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
            payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['get'], url_path='retrieve-bill-payment/(?P<bill_payment_id>\d+)')
    def retrieve_an_bill_payment(self, request, **kwargs):
        """
        Retrieve a bill payments. \n
        :Quickbooks-Authorization: access_token (required)
        :path_params: bill_payment_id
        :return: Returns bill payment detail.
        """
        response = self.quickbook_service.read_attachable(
            access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
            attachable_id=kwargs.get('bill_payment_id'))
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='update-bill-payment')
    def update_bill_payment(self, request):
        """
        Update a bill payments. \n
        :Quickbooks-Authorization: access_token (required)
        :body_params: PrivateNote, TotalAmt, PayType, Note,TxnDate, PayType, id, TotalAmt
        :body_params: VendorRef:{name, value}
        :body_params: Line:{Amount, LinkedTxn:{TxnId, TxnType}}
        :body_params: CheckPayment:{BankAccountRef:{name, value}}
        :return: Returns details about updated bill payments.
       """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.update_a_bill_payment(
            access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
            payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='create-payment')
    def create_payment(self, request):
        """
        Create a payment. \n
        :Quickbooks-Authorization: access_token (required)
        :body_params: TotalAmt,
        :body_params: CustomerRef:{value}
        :return: Returns details about created payment.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.create_payment(access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
                                                         payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='delete-payment')
    def delete_payment(self, request):
        """
        Delete a payment. \n
        :Quickbooks-Authorization: access_token (required)
        :body_params: SyncToken, Id
        :return: Returns details about deleted payment.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.delete_payment(access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
                                                         payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='void-payment')
    def void_payment(self, request):
        """
        Void a payment. \n
        :Quickbooks-Authorization: access_token (required)
        :body_params: SyncToken, Id, sparse
        :return: Returns details about voided payment.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.void_payment(access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
                                                       payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['get'], url_path='read-payment/(?P<payment_id>\d+)')
    def read_payment(self, request, *args, **kwargs):
        """
        Retrieve a payment. \n
        :Quickbooks-Authorization: access_token (required)
        :path_params: payment_id
        :return: Returns details about retrieved payment.
        """
        response = self.quickbook_service.read_payment(access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
                                                       payment_id=kwargs.get('payment_id'))
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='send-payment/(?P<payment_id>\d+)')
    def send_payment(self, request, *args, **kwargs):
        """
        Send payment. \n
        :Quickbooks-Authorization: access_token (required)
        :path_params: payment_id
        :query_params: receiver_email
        :return: Send the payment and return its details.
        """
        response = self.quickbook_service.send_payment(access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
                                                       payment_id=kwargs.get('payment_id'),
                                                       receiver_email=request.GET.get('receiver_email'))
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='create-customer')
    def create_customer(self, request):
        """
        Create a customer. \n
        :Quickbooks-Authorization: access_token (required)
        :body_params: FullyQualifiedName, DisplayName, Notes, GivenName, Title
        :body_params: PrimaryEmailAddr:{Address}
        :body_params: PrimaryPhone:{FreeFormNumber}
        :return: Returns details about created customer.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.create_customer(
            access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
            payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['get'], url_path='read-customer/(?P<customer_id>\d+)')
    def read_customer(self, request, *args, **kwargs):
        """
        Retrieve customer. \n
        :Quickbooks-Authorization: access_token (required)
        :path_params: customer_id
        :return: Return detail about retrieved customer .
        """
        response = self.quickbook_service.read_customer(access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
                                                        customer_id=kwargs.get('customer_id'))
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='update-customer')
    def update_customer(self, request):
        """
        Update a customer. \n
        :Quickbooks-Authorization: access_token (required)
        :body_params: FullyQualifiedName, DisplayName, Notes, GivenName, Title, Id, domain, BalanceWithJobs, Active
        sparse, SyncToken, CompanyName, Balance, Taxable
        :body_params: PrimaryEmailAddr:{Address}
        :body_params: PrimaryPhone:{FreeFormNumber}
        :return: Returns details about updated customer.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.update_customer(
            access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
            payload=serializer.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='create-invoice')
    def create_invoice(self, request):
        """
        Create an invoice. \n
        :Quickbooks-Authorization: access_token (required)
        :body_params: Line:{DetailType, Amount, SalesItemLineDetail:{ItemRef}}
        :body_params: CustomerRef:{value}
        :return: Returns details about created invoice.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.create_invoice(access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
                                                         payload=request.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='delete-invoice')
    def delete_invoice(self, request):
        """
        Delete an invoice. \n
        :Quickbooks-Authorization: access_token (required)
        :body_params: SyncToken, Id
        :return: Returns detail about deleted invoice.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.delete_invoice(access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
                                                         payload=request.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='void-invoice')
    def void_invoice(self, request):
        """
        Void an invoice. \n
        :Quickbooks-Authorization: access_token (required)
        :body_params: SyncToken, Id
        :return: Returns detail about voided invoice.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.void_invoice(access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
                                                       payload=request.data)
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['get'], url_path='read-invoice/(?P<invoice_id>\d+)')
    def read_invoice(self, request, *args, **kwargs):
        """
        Retrieve an invoice. \n
        :Quickbooks-Authorization: access_token (required)
        :path_params: invoice_id
        :return: Returns detail about retrieved invoice.
        """
        response = self.quickbook_service.read_invoice(access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
                                                       invoice_id=kwargs.get('invoice_id'))
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='send-invoice/(?P<invoice_id>\d+)')
    def send_invoice(self, request, *args, **kwargs):
        """
        Send an invoice. \n
        :Quickbooks-Authorization: access_token (required)
        :path_params: invoice_id
        :query_params: receiver_email
        :return: Send teh invoice and returns its detail.
        """
        response = self.quickbook_service.send_invoice(access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
                                                       invoice_id=kwargs.get('invoice_id'),
                                                       receiver_email=request.GET.get('receiver_email'))
        return Response(data=response.get("data"), status=response.get("status_code"))

    @action(detail=False, methods=['post'], url_path='update-invoice')
    def update_invoice(self, request):
        """
        Update an invoice. \n
        :Quickbooks-Authorization: access_token (required)
        :body_params: Id, DocNumber, SyncToken, domain, EmailStatus,sparse,ApplyTaxAfterDiscount,Balance, TotalAmt, DueDate, TxnDate
        :body_params: Line:{DetailType, Amount, SalesItemLineDetail:{ItemRef}}
        :body_params: CustomerRef:{value}
        :return: Returns details about created invoice.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.quickbook_service.update_invoice(access_token=request.META.get("HTTP_QUICKBOOKS_AUTHORIZATION"),
                                                         payload=request.data)
        return Response(data=response.get("data"), status=response.get("status_code"))
