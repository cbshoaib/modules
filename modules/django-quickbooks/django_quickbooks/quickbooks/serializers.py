from rest_framework import serializers


class AccessTokenSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)


class CreateAccountSerializer(serializers.Serializer):
    Name = serializers.CharField(required=True)
    AccountType = serializers.CharField(required=True)


class UpdateAccountSerializer(serializers.Serializer):
    Id = serializers.CharField(required=True, max_length=256)
    Name = serializers.CharField(required=True, max_length=256)
    FullyQualifiedName = serializers.CharField(max_length=256, required=False)
    domain = serializers.CharField(max_length=256, required=False)
    SubAccount = serializers.BooleanField(default=False, required=False)
    Description = serializers.CharField(max_length=256, required=False)
    Classification = serializers.CharField(max_length=256, required=False)
    AccountSubType = serializers.CharField(max_length=256, required=False)
    AccountType = serializers.CharField(max_length=256, required=False)
    SyncToken = serializers.CharField(max_length=256, required=False)
    CurrentBalanceWithSubAccounts = serializers.FloatField()
    CurrentBalance = serializers.FloatField()
    sparse = serializers.BooleanField(default=False)


class EntitySerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    value = serializers.CharField(required=True)


class AttachableReferenceSerializer(serializers.Serializer):
    IncludeOnSend = serializers.BooleanField(default=False)
    EntityRef = EntitySerializer()


class CreateNoteAttachableSerializer(serializers.Serializer):
    Note = serializers.CharField(required=True)
    AttachableRef = AttachableReferenceSerializer(required=False, many=True)


class DeleteAttachableSerializer(serializers.Serializer):
    SyncToken = serializers.CharField(required=True)
    Id = serializers.CharField(required=True)
    domain = serializers.CharField(required=True)
    AttachableRef = AttachableReferenceSerializer(many=True, required=False)


class UpdateAttachableSerializer(serializers.Serializer):
    SyncToken = serializers.CharField(required=True)
    Id = serializers.CharField(required=True)
    domain = serializers.CharField(required=True)
    Note = serializers.CharField(required=True)
    AttachableRef = AttachableReferenceSerializer(many=True, required=False)


class UploadAttachableSerializer(serializers.Serializer):
    FileName = serializers.FileField(required=True)


class VendorReferenceSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    value = serializers.CharField(required=True)


class BankAccountReference(serializers.Serializer):
    name = serializers.CharField(required=True)
    value = serializers.CharField(required=True)


class BankReferenceSerializer(serializers.Serializer):
    BankAccountRef = BankAccountReference()


class LinkedTxnSerializer(serializers.Serializer):
    TxnId = serializers.CharField(required=True)
    TxnType = serializers.CharField(required=True)


class LineSerializer(serializers.Serializer):
    Amount = serializers.FloatField()
    LinkedTxn = LinkedTxnSerializer(many=True)


class CreateBillPaymentSerializer(serializers.Serializer):
    PrivateNote = serializers.CharField(required=False)
    TotalAmt = serializers.FloatField(required=True)
    PayType = serializers.CharField(required=True)
    VendorRef = VendorReferenceSerializer(required=True)
    Line = LineSerializer(many=True)
    CheckPayment = BankReferenceSerializer()


class VoidBillPaymentSerializer(serializers.Serializer):
    SyncToken = serializers.CharField(required=True)
    Id = serializers.CharField(required=True)
    sparse = serializers.BooleanField()


class DeleteBillPaymentSerializer(serializers.Serializer):
    SyncToken = serializers.CharField(required=True)
    Id = serializers.CharField(required=True)


class UpdateBillPaymentSerializer(serializers.Serializer):
    PrivateNote = serializers.CharField(required=False)
    SyncToken = serializers.CharField(required=False)
    domain = serializers.CharField(required=False)
    TxnDate = serializers.DateField(required=False)
    Id = serializers.CharField(required=True)
    TotalAmt = serializers.FloatField(required=True)
    PayType = serializers.CharField(required=True)
    VendorRef = VendorReferenceSerializer(required=True)
    Line = LineSerializer(many=True)
    CheckPayment = BankReferenceSerializer()


class CustomerReferenceSerializer(serializers.Serializer):
    value = serializers.CharField(required=True)


class PaymentSerializer(serializers.Serializer):
    TotalAmt = serializers.FloatField(required=True)
    CustomerRef = CustomerReferenceSerializer(required=True)


class DeletePaymentSerializer(serializers.Serializer):
    SyncToken = serializers.CharField(required=True)
    Id = serializers.CharField(required=True)


class VoidPaymentSerializer(serializers.Serializer):
    SyncToken = serializers.CharField(required=True)
    Id = serializers.CharField(required=True)
    sparse = serializers.BooleanField(required=True)


class CustomerEmailSerializer(serializers.Serializer):
    Address = serializers.EmailField(required=True)


class CustomerPhoneSerializer(serializers.Serializer):
    FreeFormNumber = serializers.CharField()


class CustomerBillAddressSerializer(serializers.Serializer):
    CountrySubDivisionCode = serializers.CharField()
    City = serializers.CharField()
    PostalCode = serializers.CharField()
    Line1 = serializers.CharField()
    Country = serializers.CharField()


class CustomerSerializer(serializers.Serializer):
    FullyQualifiedName = serializers.CharField(required=True)
    DisplayName = serializers.CharField(required=True)
    Notes = serializers.CharField(required=True)
    GivenName = serializers.CharField(required=True)
    Title = serializers.CharField(required=False)
    PrimaryEmailAddr = CustomerEmailSerializer()
    PrimaryPhone = CustomerPhoneSerializer()


class UpdateCustomerSerializer(serializers.Serializer):
    FullyQualifiedName = serializers.CharField(required=False)
    DisplayName = serializers.CharField(required=False)
    Id = serializers.CharField(required=True)
    domain = serializers.CharField(required=False)
    BalanceWithJobs = serializers.FloatField(required=False)
    Notes = serializers.CharField(required=False)
    GivenName = serializers.CharField(required=False)
    Active = serializers.BooleanField(required=False)
    sparse = serializers.BooleanField(required=False)
    Title = serializers.CharField(required=False)
    SyncToken = serializers.CharField(required=False)
    CompanyName = serializers.CharField(required=False)
    Balance = serializers.FloatField(required=False)
    Taxable = serializers.BooleanField(required=False)
    PrimaryEmailAddr = CustomerEmailSerializer()
    PrimaryPhone = CustomerPhoneSerializer()


class ItemReferenceSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()


class SalesItemSerializer(serializers.Serializer):
    ItemRef = ItemReferenceSerializer()


class InvoiceLineSerializer(serializers.Serializer):
    DetailType = serializers.CharField(required=True)
    Amount = serializers.FloatField()
    SalesItemLineDetail = SalesItemSerializer(required=True)


class CreateInvoiceSerializer(serializers.Serializer):
    Line = InvoiceLineSerializer(many=True, required=True)
    CustomerRef = CustomerReferenceSerializer(required=True)


class DeleteInvoiceSerializer(serializers.Serializer):
    SyncToken = serializers.CharField(required=True)
    Id = serializers.CharField(required=True)


class VoidInvoiceSerializer(serializers.Serializer):
    SyncToken = serializers.CharField(required=True)
    Id = serializers.CharField(required=True)


class UpdateInvoiceSerializer(serializers.Serializer):
    Line = InvoiceLineSerializer(many=True, required=True)
    CustomerRef = CustomerReferenceSerializer(required=True)
    Id = serializers.CharField(required=True)
    DocNumber = serializers.CharField(required=False)
    SyncToken = serializers.CharField(required=False)
    domain = serializers.CharField(required=False)
    EmailStatus = serializers.CharField(required=False)
    sparse = serializers.BooleanField(required=False)
    ApplyTaxAfterDiscount = serializers.BooleanField(required=False)
    Balance = serializers.FloatField(required=False)
    TotalAmt = serializers.FloatField(required=False)
    DueDate = serializers.DateField(required=False)
    TxnDate = serializers.DateField(required=False)
