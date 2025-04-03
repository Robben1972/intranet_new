import os

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Upload a file",
        operation_description="Uploads a file to the specified service directory.",
        manual_parameters=[
            openapi.Parameter(
                'file',
                openapi.IN_FORM,
                description="File to upload",
                type=openapi.TYPE_FILE,
                required=True,
            ),
            openapi.Parameter(
                'service',
                openapi.IN_FORM,
                description="Service name",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            201: openapi.Response(
                description="File uploaded successfully",
                examples={"application/json": {"file_path": "/media/service_name/filename.ext"}},
            ),
            400: "Bad Request",
        },
    )
    def post(self, request):
        file = request.FILES.get('file')
        service = request.POST.get('service')

        if not file or not service:
            return Response({'error': 'Both file and service are required.'}, status=status.HTTP_400_BAD_REQUEST)

        media_root = settings.MEDIA_ROOT
        service_dir = os.path.join(media_root, service)

        if not os.path.exists(service_dir):
            os.makedirs(service_dir)

        fs = FileSystemStorage(location=service_dir)
        filename = fs.save(file.name, file)

        return Response({'file_path': filename}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Download a file",
        operation_description="Downloads a file from the specified service directory.",
        manual_parameters=[
            openapi.Parameter(
                'service', openapi.IN_QUERY, description="Service name", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'filename', openapi.IN_QUERY, description="Name of the file", type=openapi.TYPE_STRING, required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="File downloaded successfully",
                content={"application/octet-stream": {}},
            ),
            404: "File not found",
        },
    )
    def get(self, request):
        service = request.GET.get('service') or request.data.get('service')
        filename = request.GET.get('filename') or request.data.get('filename')

        if not service or not filename:
            return Response({'error': 'Both service and filename are required.'}, status=status.HTTP_400_BAD_REQUEST)

        media_root = settings.MEDIA_ROOT
        file_path = os.path.join(media_root, service, filename)

        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True)
        else:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)