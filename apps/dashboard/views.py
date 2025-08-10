from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework import status,permissions
from core.response import *
from .models import *
from .serializers import *
from django.db.models import Q

class DashboardView(View):
    def get(self, request):
        return render(request, 'dashboard/dashboard.html')
    


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



