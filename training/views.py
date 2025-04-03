from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
from django.conf import settings
from django.http import Http404
from .serializers import TrainingSerializerEN, TrainingSerializerRU, TrainingSerializerUZ
from .models import TrainingModel

class TrainingListViewEN(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Get list of trainings in English",
        responses={200: TrainingSerializerEN(many=True)}
    )
    def get(self, request):
        trainings = TrainingModel.objects.all()
        serializer = TrainingSerializerEN(trainings, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create training in English",
        operation_description="Upload files and create a training entry in English.",
        manual_parameters=[
            openapi.Parameter('title_en', openapi.IN_FORM, description="Title in English", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('description_en', openapi.IN_FORM, description="Description in English", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('department_en', openapi.IN_FORM, description="Department in English", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('location_en', openapi.IN_FORM, description="Location in English", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('category_en', openapi.IN_FORM, description="Category in English", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('image', openapi.IN_FORM, description="Image file to upload", type=openapi.TYPE_FILE, required=True),
            openapi.Parameter('start_time', openapi.IN_FORM, description="Start time", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_time', openapi.IN_FORM, description="End time", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('date', openapi.IN_FORM, description="Date", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('video', openapi.IN_FORM, description="Video file to upload", type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('attachments', openapi.IN_FORM, description="Attachment file to upload", type=openapi.TYPE_FILE, required=False),
        ],
        responses={
            201: TrainingSerializerEN,
            400: "Bad Request",
        }
    )
    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'Image is required.'}, status=status.HTTP_400_BAD_REQUEST)

        fileapp_url = f"{settings.FILEAPP_URL}/"
        fileapp_response = requests.post(fileapp_url, files={'file': image}, data={'service': 'training'})
        if fileapp_response.status_code != 201:
            return Response({'error': 'Failed to upload image.'}, status=status.HTTP_400_BAD_REQUEST)
        image_path = fileapp_response.json().get('file_path')

        data = request.data.copy()
        data['image'] = image_path

        video = request.FILES.get('video')
        if video:
            fileapp_response = requests.post(fileapp_url, files={'file': video}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload video.'}, status=status.HTTP_400_BAD_REQUEST)
            data['video'] = fileapp_response.json().get('file_path')

        # Handle attachments upload if present
        attachments = request.FILES.get('attachments')
        if attachments:
            fileapp_response = requests.post(fileapp_url, files={'file': attachments}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload attachments.'}, status=status.HTTP_400_BAD_REQUEST)
            data['attachments'] = fileapp_response.json().get('file_path')

        serializer = TrainingSerializerEN(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TrainingDetailViewEN(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return TrainingModel.objects.get(pk=pk)
        except TrainingModel.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="Get a specific training in English",
        responses={
            200: TrainingSerializerEN(),
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        training = self.get_object(pk)
        serializer = TrainingSerializerEN(training)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update a training in English",
        operation_description="Update an existing training with optional file uploads in English.",
        manual_parameters=[
            openapi.Parameter('title_en', openapi.IN_FORM, description="Title in English", type=openapi.TYPE_STRING),
            openapi.Parameter('description_en', openapi.IN_FORM, description="Description in English", type=openapi.TYPE_STRING),
            openapi.Parameter('department_en', openapi.IN_FORM, description="Department in English", type=openapi.TYPE_STRING),
            openapi.Parameter('location_en', openapi.IN_FORM, description="Location in English", type=openapi.TYPE_STRING),
            openapi.Parameter('category_en', openapi.IN_FORM, description="Category in English", type=openapi.TYPE_STRING),
            openapi.Parameter('image', openapi.IN_FORM, description="Image file to upload", type=openapi.TYPE_FILE),
            openapi.Parameter('start_time', openapi.IN_FORM, description="Start time", type=openapi.TYPE_STRING),
            openapi.Parameter('end_time', openapi.IN_FORM, description="End time", type=openapi.TYPE_STRING),
            openapi.Parameter('date', openapi.IN_FORM, description="Date", type=openapi.TYPE_STRING),
            openapi.Parameter('video', openapi.IN_FORM, description="Video file to upload", type=openapi.TYPE_FILE),
            openapi.Parameter('attachments', openapi.IN_FORM, description="Attachment file to upload", type=openapi.TYPE_FILE),
        ],
        responses={
            200: TrainingSerializerEN,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        training = self.get_object(pk)
        data = request.data.copy()
        fileapp_url = f"{settings.FILEAPP_URL}/"

        image = request.FILES.get('image')
        if image:
            fileapp_response = requests.post(fileapp_url, files={'file': image}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload image.'}, status=status.HTTP_400_BAD_REQUEST)
            data['image'] = fileapp_response.json().get('file_path')

        # Handle video upload if present
        video = request.FILES.get('video')
        if video:
            fileapp_response = requests.post(fileapp_url, files={'file': video}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload video.'}, status=status.HTTP_400_BAD_REQUEST)
            data['video'] = fileapp_response.json().get('file_path')

        # Handle attachments upload if present
        attachments = request.FILES.get('attachments')
        if attachments:
            fileapp_response = requests.post(fileapp_url, files={'file': attachments}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload attachments.'}, status=status.HTTP_400_BAD_REQUEST)
            data['attachments'] = fileapp_response.json().get('file_path')

        serializer = TrainingSerializerEN(training, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a training in English",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        training = self.get_object(pk)
        training.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Russian (RU) Version
class TrainingListViewRU(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Get list of trainings in Russian",
        responses={200: TrainingSerializerRU(many=True)}
    )
    def get(self, request):
        trainings = TrainingModel.objects.all()
        serializer = TrainingSerializerRU(trainings, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create training in Russian",
        operation_description="Upload files and create a training entry in Russian.",
        manual_parameters=[
            openapi.Parameter('title_ru', openapi.IN_FORM, description="Title in Russian", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('description_ru', openapi.IN_FORM, description="Description in Russian", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('department_ru', openapi.IN_FORM, description="Department in Russian", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('location_ru', openapi.IN_FORM, description="Location in Russian", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('category_ru', openapi.IN_FORM, description="Category in Russian", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('image', openapi.IN_FORM, description="Image file to upload", type=openapi.TYPE_FILE, required=True),
            openapi.Parameter('start_time', openapi.IN_FORM, description="Start time", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_time', openapi.IN_FORM, description="End time", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('date', openapi.IN_FORM, description="Date", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('video', openapi.IN_FORM, description="Video file to upload", type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('attachments', openapi.IN_FORM, description="Attachment file to upload", type=openapi.TYPE_FILE, required=False),
        ],
        responses={
            201: TrainingSerializerRU,
            400: "Bad Request",
        }
    )
    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'Image is required.'}, status=status.HTTP_400_BAD_REQUEST)

        fileapp_url = f"{settings.FILEAPP_URL}/"
        fileapp_response = requests.post(fileapp_url, files={'file': image}, data={'service': 'training'})
        if fileapp_response.status_code != 201:
            return Response({'error': 'Failed to upload image.'}, status=status.HTTP_400_BAD_REQUEST)
        image_path = fileapp_response.json().get('file_path')

        data = request.data.copy()
        data['image'] = image_path

        video = request.FILES.get('video')
        if video:
            fileapp_response = requests.post(fileapp_url, files={'file': video}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload video.'}, status=status.HTTP_400_BAD_REQUEST)
            data['video'] = fileapp_response.json().get('file_path')

        attachments = request.FILES.get('attachments')
        if attachments:
            fileapp_response = requests.post(fileapp_url, files={'file': attachments}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload attachments.'}, status=status.HTTP_400_BAD_REQUEST)
            data['attachments'] = fileapp_response.json().get('file_path')

        serializer = TrainingSerializerRU(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TrainingDetailViewRU(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return TrainingModel.objects.get(pk=pk)
        except TrainingModel.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="Get a specific training in Russian",
        responses={
            200: TrainingSerializerRU(),
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        training = self.get_object(pk)
        serializer = TrainingSerializerRU(training)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update a training in Russian",
        operation_description="Update an existing training with optional file uploads in Russian.",
        manual_parameters=[
            openapi.Parameter('title_ru', openapi.IN_FORM, description="Title in Russian", type=openapi.TYPE_STRING),
            openapi.Parameter('description_ru', openapi.IN_FORM, description="Description in Russian", type=openapi.TYPE_STRING),
            openapi.Parameter('department_ru', openapi.IN_FORM, description="Department in Russian", type=openapi.TYPE_STRING),
            openapi.Parameter('location_ru', openapi.IN_FORM, description="Location in Russian", type=openapi.TYPE_STRING),
            openapi.Parameter('category_ru', openapi.IN_FORM, description="Category in Russian", type=openapi.TYPE_STRING),
            openapi.Parameter('image', openapi.IN_FORM, description="Image file to upload", type=openapi.TYPE_FILE),
            openapi.Parameter('start_time', openapi.IN_FORM, description="Start time", type=openapi.TYPE_STRING),
            openapi.Parameter('end_time', openapi.IN_FORM, description="End time", type=openapi.TYPE_STRING),
            openapi.Parameter('date', openapi.IN_FORM, description="Date", type=openapi.TYPE_STRING),
            openapi.Parameter('video', openapi.IN_FORM, description="Video file to upload", type=openapi.TYPE_FILE),
            openapi.Parameter('attachments', openapi.IN_FORM, description="Attachment file to upload", type=openapi.TYPE_FILE),
        ],
        responses={
            200: TrainingSerializerRU,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        training = self.get_object(pk)
        data = request.data.copy()
        fileapp_url = f"{settings.FILEAPP_URL}/"

        image = request.FILES.get('image')
        if image:
            fileapp_response = requests.post(fileapp_url, files={'file': image}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload image.'}, status=status.HTTP_400_BAD_REQUEST)
            data['image'] = fileapp_response.json().get('file_path')

        video = request.FILES.get('video')
        if video:
            fileapp_response = requests.post(fileapp_url, files={'file': video}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload video.'}, status=status.HTTP_400_BAD_REQUEST)
            data['video'] = fileapp_response.json().get('file_path')

        attachments = request.FILES.get('attachments')
        if attachments:
            fileapp_response = requests.post(fileapp_url, files={'file': attachments}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload attachments.'}, status=status.HTTP_400_BAD_REQUEST)
            data['attachments'] = fileapp_response.json().get('file_path')

        serializer = TrainingSerializerRU(training, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a training in Russian",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        training = self.get_object(pk)
        training.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TrainingListViewUZ(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Get list of trainings in Uzbek",
        responses={200: TrainingSerializerUZ(many=True)}
    )
    def get(self, request):
        trainings = TrainingModel.objects.all()
        serializer = TrainingSerializerUZ(trainings, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create training in Uzbek",
        operation_description="Upload files and create a training entry in Uzbek.",
        manual_parameters=[
            openapi.Parameter('title_uz', openapi.IN_FORM, description="Title in Uzbek", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('description_uz', openapi.IN_FORM, description="Description in Uzbek", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('department_uz', openapi.IN_FORM, description="Department in Uzbek", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('location_uz', openapi.IN_FORM, description="Location in Uzbek", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('category_uz', openapi.IN_FORM, description="Category in Uzbek", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('image', openapi.IN_FORM, description="Image file to upload", type=openapi.TYPE_FILE, required=True),
            openapi.Parameter('start_time', openapi.IN_FORM, description="Start time", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_time', openapi.IN_FORM, description="End time", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('date', openapi.IN_FORM, description="Date", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('video', openapi.IN_FORM, description="Video file to upload", type=openapi.TYPE_FILE, required=False),
            openapi.Parameter('attachments', openapi.IN_FORM, description="Attachment file to upload", type=openapi.TYPE_FILE, required=False),
        ],
        responses={
            201: TrainingSerializerUZ,
            400: "Bad Request",
        }
    )
    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'Image is required.'}, status=status.HTTP_400_BAD_REQUEST)

        fileapp_url = f"{settings.FILEAPP_URL}/"
        fileapp_response = requests.post(fileapp_url, files={'file': image}, data={'service': 'training'})
        if fileapp_response.status_code != 201:
            return Response({'error': 'Failed to upload image.'}, status=status.HTTP_400_BAD_REQUEST)
        image_path = fileapp_response.json().get('file_path')

        data = request.data.copy()
        data['image'] = image_path

        video = request.FILES.get('video')
        if video:
            fileapp_response = requests.post(fileapp_url, files={'file': video}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload video.'}, status=status.HTTP_400_BAD_REQUEST)
            data['video'] = fileapp_response.json().get('file_path')

        attachments = request.FILES.get('attachments')
        if attachments:
            fileapp_response = requests.post(fileapp_url, files={'file': attachments}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload attachments.'}, status=status.HTTP_400_BAD_REQUEST)
            data['attachments'] = fileapp_response.json().get('file_path')

        serializer = TrainingSerializerUZ(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TrainingDetailViewUZ(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return TrainingModel.objects.get(pk=pk)
        except TrainingModel.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="Get a specific training in Uzbek",
        responses={
            200: TrainingSerializerUZ(),
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        training = self.get_object(pk)
        serializer = TrainingSerializerUZ(training)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update a training in Uzbek",
        operation_description="Update an existing training with optional file uploads in Uzbek.",
        manual_parameters=[
            openapi.Parameter('title_uz', openapi.IN_FORM, description="Title in Uzbek", type=openapi.TYPE_STRING),
            openapi.Parameter('description_uz', openapi.IN_FORM, description="Description in Uzbek", type=openapi.TYPE_STRING),
            openapi.Parameter('department_uz', openapi.IN_FORM, description="Department in Uzbek", type=openapi.TYPE_STRING),
            openapi.Parameter('location_uz', openapi.IN_FORM, description="Location in Uzbek", type=openapi.TYPE_STRING),
            openapi.Parameter('category_uz', openapi.IN_FORM, description="Category in Uzbek", type=openapi.TYPE_STRING),
            openapi.Parameter('image', openapi.IN_FORM, description="Image file to upload", type=openapi.TYPE_FILE),
            openapi.Parameter('start_time', openapi.IN_FORM, description="Start time", type=openapi.TYPE_STRING),
            openapi.Parameter('end_time', openapi.IN_FORM, description="End time", type=openapi.TYPE_STRING),
            openapi.Parameter('date', openapi.IN_FORM, description="Date", type=openapi.TYPE_STRING),
            openapi.Parameter('video', openapi.IN_FORM, description="Video file to upload", type=openapi.TYPE_FILE),
            openapi.Parameter('attachments', openapi.IN_FORM, description="Attachment file to upload", type=openapi.TYPE_FILE),
        ],
        responses={
            200: TrainingSerializerUZ,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        training = self.get_object(pk)
        data = request.data.copy()
        fileapp_url = f"{settings.FILEAPP_URL}/"

        image = request.FILES.get('image')
        if image:
            fileapp_response = requests.post(fileapp_url, files={'file': image}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload image.'}, status=status.HTTP_400_BAD_REQUEST)
            data['image'] = fileapp_response.json().get('file_path')

        video = request.FILES.get('video')
        if video:
            fileapp_response = requests.post(fileapp_url, files={'file': video}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload video.'}, status=status.HTTP_400_BAD_REQUEST)
            data['video'] = fileapp_response.json().get('file_path')

        attachments = request.FILES.get('attachments')
        if attachments:
            fileapp_response = requests.post(fileapp_url, files={'file': attachments}, data={'service': 'training'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload attachments.'}, status=status.HTTP_400_BAD_REQUEST)
            data['attachments'] = fileapp_response.json().get('file_path')

        serializer = TrainingSerializerUZ(training, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a training in Uzbek",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        training = self.get_object(pk)
        training.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)