from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework import status,permissions
from core.response import *
from .models import *
from .serializers import *
from django.db.models import Q
import requests
import string
import random
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .tasks import process_file_word_count
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, View):
    login_url = '/login/'       
    redirect_field_name = None 

    def get(self, request):
        current_user = request.user
        context = {
            "paid": current_user.is_paid_user if current_user else None
        }
        return render(request, 'dashboard/dashboard.html', context=context)
class PaymentHistoryView(LoginRequiredMixin,View):
    login_url = '/login/'       
    redirect_field_name = None 
    
    def get(self, request):
        current_user = request.user
        
        context={
            "current_user": current_user
            
        }
        return render(request, 'payment/payment_history.html',context=context)
    
class ActivityView(LoginRequiredMixin, View):
    login_url = '/login/'       
    redirect_field_name = None 

    def get(self, request):
        current_user = request.user
        
        context={
            "current_user": current_user
            
        }
        return render(request, 'dashboard/activity.html',context=context)
    


class FileCRUDView(APIView):
    """
    Handles CRUD operations for FileUpload.
    
    Methods:
    - GET: Retrieve all file upload or a specific file upload by ID.
    - PATCH: Partially update a file upload.
    - DELETE: Delete a file.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileUploadSerializer
    queryset = FileUpload.objects.all()

    def get(self, request):
        """
        Retrieve a specific file upload by ID (if provided),
        or return a list of all file.
        """
        file_id = request.query_params.get("file_id")
        current_user = request.user

        if file_id:
            # Try to fetch specific file by ID
            try:
                file = self.queryset.get(id=file_id)
                serializer = self.serializer_class(file)
                return CustomApiResponse(
                    status="success",
                    message="File retrieved successfully.",
                    data=serializer.data,
                    code=status.HTTP_200_OK
                ).get_response()
            except FileUpload.DoesNotExist:
                # If file not found, return custom 404 response
                return CustomApiResponse(
                    status="error",
                    message="File not found.",
                    data={},
                    code=status.HTTP_404_NOT_FOUND
                ).get_response()
        else:
            # If no file_id is given, return all files
            if current_user.is_superuser or current_user.is_staff:
                files = self.queryset.all().order_by("-id")
            else:
                files = self.queryset.filter(user=current_user).order_by("-id")

            serializer = self.serializer_class(files, many=True)
            return CustomApiResponse(
                status="success",
                message="All file retrieved successfully.",
                data=serializer.data,
                code=status.HTTP_200_OK
            ).get_response()
        

    def patch(self, request):
        """
        Partial update of a file.
        Requires 'file_id' query parameter.
        """
        file_id = request.query_params.get("file_id")
        if not file_id:
            return CustomApiResponse(
                status="error",
                message="File ID is required for update.",
                data={},
                code=status.HTTP_400_BAD_REQUEST
            ).get_response()

        try:
            file = self.queryset.get(id=file_id)
        except FileUpload.DoesNotExist:
            return CustomApiResponse(
                status="error",
                message="File not found.",
                data={},
                code=status.HTTP_404_NOT_FOUND
            ).get_response()

        serializer = self.serializer_class(file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomApiResponse(
                status="success",
                message="File updated successfully.",
                data=serializer.data,
                code=status.HTTP_200_OK
            ).get_response()

        return CustomApiResponse(
            status="error",
            message="File update failed.",
            data=serializer.errors,
            code=status.HTTP_400_BAD_REQUEST
        ).get_response()
    

    def delete(self, request):
        """
        Delete a file.
        Requires 'file_id' query parameter.
        """
        file_id = request.query_params.get("file_id")
        if not file_id:
            return CustomApiResponse(
                status="error",
                message="File ID is required for deletion.",
                data={},
                code=status.HTTP_400_BAD_REQUEST
            ).get_response()

        try:
            file = self.queryset.get(id=file_id)
            file.delete()
            return CustomApiResponse(
                status="success",
                message="File deleted successfully.",
                data={},
                code=status.HTTP_204_NO_CONTENT
            ).get_response()
        except FileUpload.DoesNotExist:
            return CustomApiResponse(
                status="error",
                message="File not found.",
                data={},
                code=status.HTTP_404_NOT_FOUND
            ).get_response()


class FileUploadView(APIView):
    """
    Handles Create operations for FileUpload.
    
    Methods:
    - POST: Create a new file upload.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileUploadSerializer
    queryset = FileUpload.objects.all()

    
    def post(self, request):
        current_user = request.user
        data = request.data.copy()
        data["user"] = current_user.id
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            data['filename'] = uploaded_file.name 

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            file_ins = serializer.save()
            process_file_word_count(file_ins.id)
            return CustomApiResponse(
                status='success',
                message='File successful!',
                data=serializer.data,
                code=status.HTTP_201_CREATED
            ).get_response()
        
        return CustomApiResponse(
            status='error',
            message='File Create failed',
            data=serializer.errors,
            code=status.HTTP_400_BAD_REQUEST
        ).get_response()

class TransactionView(APIView):
    """
    Handles operations for Transaction.
    
    Methods:
    - GET: Get all transaction upload or a specific transaction.
    - DELETE: Delete a file.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentTransactionSerializer
    queryset = PaymentTransaction.objects.all()

    def get(self, request):
        current_user = request.user

        transaction_id = request.query_params.get("transaction_id")

        if transaction_id:
            # Try to fetch specific transaction by ID
            try:
                file = self.queryset.get(id=transaction_id)
                serializer = self.serializer_class(file)
                return CustomApiResponse(
                    status="success",
                    message="Transaction Get successfully.",
                    data=serializer.data,
                    code=status.HTTP_200_OK
                ).get_response()
            except FileUpload.DoesNotExist:
                # If transaction not found, return custom 404 response
                return CustomApiResponse(
                    status="error",
                    message="Transaction not found.",
                    data={},
                    code=status.HTTP_404_NOT_FOUND
                ).get_response()
        else:
            # If no transaction_id is given, return all transaction
            if current_user.is_superuser or current_user.is_staff:
                transaction = self.queryset.all().order_by("-id")
            else:
                transaction = self.queryset.filter(user=current_user).order_by("-id")

            serializer = self.serializer_class(transaction, many=True)
            ser_data = serializer.data
            data = {
                "data":ser_data,
                "is_superuser":current_user.is_superuser

            }
            
            return CustomApiResponse(
                status="success",
                message="All transaction retrieved successfully.",
                data=data,
                code=status.HTTP_200_OK
            ).get_response()
        

    def delete(self, request):

        transaction_id = request.query_params.get("transaction_id")
        if not transaction_id:
            return CustomApiResponse(
                status="error",
                message="Transaction ID is required for deletion.",
                data={},
                code=status.HTTP_400_BAD_REQUEST
            ).get_response()

        try:
            transaction = self.queryset.get(id=transaction_id)
            transaction.delete()
            return CustomApiResponse(
                status="success",
                message="Transaction deleted successfully.",
                data={},
                code=status.HTTP_204_NO_CONTENT
            ).get_response()
        except PaymentTransaction.DoesNotExist:
            return CustomApiResponse(
                status="error",
                message="Transaction not found.",
                data={},
                code=status.HTTP_404_NOT_FOUND
            ).get_response()


class ActivityListView(APIView):
    """
    Handles CRUD operations for FileUpload.
    
    Methods:
    - GET: Retrieve all activity or a get specific activity  by ID.
   
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ActivityLogSerializer
    queryset = ActivityLog.objects.all()

    def get(self, request):
        activity_id = request.query_params.get("activity_id")
        current_user = request.user
        

        if activity_id:

            try:
                activity = self.queryset.get(id=activity_id)
                serializer = self.serializer_class(activity_id)
                return CustomApiResponse(
                    status="success",
                    message="Get All Activity successfully.",
                    data=serializer.data,
                    code=status.HTTP_200_OK
                ).get_response()
            except FileUpload.DoesNotExist:
                
                return CustomApiResponse(
                    status="error",
                    message="Activity not found.",
                    data={},
                    code=status.HTTP_404_NOT_FOUND
                ).get_response()
        else:
            if current_user.is_superuser or current_user.is_staff:
                activity = self.queryset.all().order_by("-id")
            else:
                activity = self.queryset.filter(user=current_user).order_by("-id")
        
            serializer = self.serializer_class(activity, many=True)
            return CustomApiResponse(
                status="success",
                message="Get All Activity successfully.",
                data=serializer.data,
                code=status.HTTP_200_OK
            ).get_response()


def generate_transaction_id():
    while True:
        random_part = ''.join(random.choices(string.digits, k=6))  # 6 digit random number
        transaction_id = f'aamarpay{random_part}'
        if not PaymentTransaction.objects.filter(transaction_id=transaction_id).exists():
            return transaction_id


class PaymentView(APIView):
    """
    POST: Send request to initiate payment

    """

    permission_classes = [permissions.IsAuthenticated]
    AAMARPAY_ENDPOINT = "https://sandbox.aamarpay.com/jsonpost.php"
    STORE_ID = "aamarpaytest"
    SIGNATURE_KEY = "dbb74894e82415a2f7ff0ec3a97e4183"



    def post(self, request):
        current_user = request.user
        data = request.data
        tran_id = generate_transaction_id()
        base_url = request.scheme + "://" + request.get_host()
        
        payload = {
            "store_id": self.STORE_ID,
            "signature_key": self.SIGNATURE_KEY,
            "tran_id": tran_id,
            "success_url": base_url + "/api/payment/success/",
            "fail_url": base_url + "/payment/fail/",
            "cancel_url": base_url + "/payment/cancel/",
            "amount": float(data.get("amount")),
            "currency": "BDT",
            "desc": data.get("desc"),
            "cus_name": data.get("cus_name"),
            "cus_email": current_user.email,
            "cus_phone": data.get("cus_phone"),
            "type": "json"
        }

        res = requests.post(self.AAMARPAY_ENDPOINT, json=payload)
        response_data = res.json()
        if response_data.get("result"):
            serializer = PaymentTransactionSerializer(data={
                    "user": current_user.id,
                    "transaction_id": tran_id,
                    "amount": data.get("amount"),
                    "currency": data.get("currency"),
                    "description": data.get("desc"),
                    "customer_name": data.get("cus_name"),
                    "customer_email": data.get("cus_email"),
                    "customer_phone": data.get("cus_phone"),
                    "gateway_response": {}
                })
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return CustomApiResponse(
                status='success',
                message='Successful!',
                data=response_data,
                code=status.HTTP_200_OK
            ).get_response()
        else:
            return CustomApiResponse(
                status='error',
                message='Failed',
                data=res.json(),
                code=status.HTTP_400_BAD_REQUEST
            ).get_response()
            

@csrf_exempt
def payment_success(request):
    data = request.POST 

    transaction_id = data.get("mer_txnid")

    try:
        transaction = PaymentTransaction.objects.get(transaction_id=transaction_id)
        transaction.gateway_response = data
        transaction.status = "success"
        transaction.save()
        transaction.user.is_paid_user = True
        transaction.user.save()
        

    except PaymentTransaction.DoesNotExist:
        return redirect('payment-fail')

    return render(request, 'payment/success.html',context={})



@csrf_exempt
def payment_cancel(request):
        data = request.POST 
        print(data)
        context={
           
        }
        return render(request, 'payment/cancel.html',context=context)
    
@csrf_exempt
def payment_fail(request):
        data = request.POST 
        print(data)
        context={
            
        }
        return render(request, 'payment/fail.html',context=context)
    