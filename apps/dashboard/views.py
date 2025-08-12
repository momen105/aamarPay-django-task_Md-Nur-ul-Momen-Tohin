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
from django.utils.decorators import method_decorator
import json
from django.contrib.auth.decorators import login_required



class DashboardView(View):
    def get(self, request):
        current_user = request.user
        print(current_user)
        
        context={
            "paid":False
        }
        return render(request, 'dashboard/dashboard.html',context=context)
    


class FileCRUDView(APIView):
    """
    Handles CRUD operations for FileUpload.
    
    Methods:
    - GET: Retrieve all file upload or a specific file upload by ID.
    - POST: Create a new file upload.
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
            file = self.queryset.all()
            serializer = self.serializer_class(file, many=True)
            return CustomApiResponse(
                status="success",
                message="All file retrieved successfully.",
                data=serializer.data,
                code=status.HTTP_200_OK
            ).get_response()
        

    def post(self, request):
        current_user = request.user
        data = request.data.copy()
        data["user"] = current_user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
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
            "cus_email": data.get("cus_email"),
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
    