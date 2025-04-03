from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
from django.conf import settings

from .serializers import NewsSerializerEN, NewsSerializerRU, NewsSerializerUZ
from .models import News

class NewsListViewUZ(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Get list of news in Uzbek",
        responses={200: NewsSerializerUZ(many=True)}
    )
    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializerUZ(news, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create news in Uzbek",
        operation_description="Upload an image and create a news entry in Uzbek.",
        manual_parameters=[
            openapi.Parameter(
                'title_uz', openapi.IN_FORM, description="Title in Uzbek", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'description_uz', openapi.IN_FORM, description="Description in Uzbek", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'department_uz', openapi.IN_FORM, description="Department in Uzbek", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'image',
                openapi.IN_FORM,
                description="File to upload",
                type=openapi.TYPE_FILE,
                required=True,
            ),
        ],
        responses={
            201: NewsSerializerUZ,
            400: "Bad Request",
        }
    )
    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'Image is required.'}, status=status.HTTP_400_BAD_REQUEST)

        fileapp_url = f"{settings.FILEAPP_URL}/"
        fileapp_response = requests.post(fileapp_url, files={'file': image}, data={'service': 'news'})

        if fileapp_response.status_code != 201:
            return Response({'error': 'Failed to upload image.'}, status=status.HTTP_400_BAD_REQUEST)

        image_path = fileapp_response.json().get('file_path')

        data = request.data.copy()
        data['image'] = image_path
        serializer = NewsSerializerUZ(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class NewsListViewRU(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Get list of news in Russian",
        responses={200: NewsSerializerRU(many=True)}
    )
    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializerRU(news, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create news in Russian",
        operation_description="Upload an image and create a news entry in Russian.",
        manual_parameters=[
            openapi.Parameter(
                'title_ru', openapi.IN_FORM, description="Title in Russian", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'description_ru', openapi.IN_FORM, description="Description in Russian", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'department_ru', openapi.IN_FORM, description="Department in Russian", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'image',
                openapi.IN_FORM,
                description="File to upload",
                type=openapi.TYPE_FILE,
                required=True,
            ),
        ],
        responses={
            201: NewsSerializerRU,
            400: "Bad Request",
        }
    )
    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'Image is required.'}, status=status.HTTP_400_BAD_REQUEST)

        fileapp_url = f"{settings.FILEAPP_URL}/"
        fileapp_response = requests.post(fileapp_url, files={'file': image}, data={'service': 'news'})

        if fileapp_response.status_code != 201:
            return Response({'error': 'Failed to upload image.'}, status=status.HTTP_400_BAD_REQUEST)

        image_path = fileapp_response.json().get('file_path')

        # Save news entry
        data = request.data.copy()
        data['image'] = image_path
        serializer = NewsSerializerRU(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class NewsListViewEN(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Get list of news in English",
        responses={200: NewsSerializerEN(many=True)}
    )
    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializerEN(news, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create news in English",
        operation_description="Upload an image and create a news entry in English.",
        manual_parameters=[
            openapi.Parameter(
                'title_en', openapi.IN_FORM, description="Title in English", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'description_en', openapi.IN_FORM, description="Description in English", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'department_en', openapi.IN_FORM, description="Department in English", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'image',
                openapi.IN_FORM,
                description="File to upload",
                type=openapi.TYPE_FILE,
                required=True,
            ),
        ],
        responses={
            201: NewsSerializerEN,
            400: "Bad Request",
        }
    )
    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'Image is required.'}, status=status.HTTP_400_BAD_REQUEST)

        fileapp_url = f"{settings.FILEAPP_URL}/"
        fileapp_response = requests.post(fileapp_url, files={'file': image}, data={'service': 'news'})

        if fileapp_response.status_code != 201:
            return Response({'error': 'Failed to upload image.'}, status=status.HTTP_400_BAD_REQUEST)

        image_path = fileapp_response.json().get('file_path')

        # Save news entry
        data = request.data.copy()
        data['image'] = image_path
        serializer = NewsSerializerEN(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    


class NewsDetailViewUZ(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return News.objects.get(pk=pk)
        except News.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="Get a specific news item in Uzbek",
        responses={
            200: NewsSerializerUZ(),
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        news = self.get_object(pk)
        serializer = NewsSerializerUZ(news)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update a news item in Uzbek",
        operation_description="Update an existing news item with optional image upload in Uzbek.",
        manual_parameters=[
            openapi.Parameter(
                'title_uz', openapi.IN_FORM, description="Title in Uzbek", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'description_uz', openapi.IN_FORM, description="Description in Uzbek", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'department_uz', openapi.IN_FORM, description="Department in Uzbek", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'image', openapi.IN_FORM, description="File to upload", type=openapi.TYPE_FILE
            ),
        ],
        responses={
            200: NewsSerializerUZ,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        news = self.get_object(pk)
        data = request.data.copy()

        image = request.FILES.get('image')
        if image:
            fileapp_url = f"{settings.FILEAPP_URL}/"
            fileapp_response = requests.post(fileapp_url, files={'file': image}, data={'service': 'news'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload image.'}, status=status.HTTP_400_BAD_REQUEST)
            data['image'] = fileapp_response.json().get('file_path')

        serializer = NewsSerializerUZ(news, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a news item in Uzbek",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        news = self.get_object(pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewsDetailViewRU(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return News.objects.get(pk=pk)
        except News.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="Get a specific news item in Russian",
        responses={
            200: NewsSerializerRU(),
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        news = self.get_object(pk)
        serializer = NewsSerializerRU(news)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update a news item in Russian",
        operation_description="Update an existing news item with optional image upload in Russian.",
        manual_parameters=[
            openapi.Parameter(
                'title_ru', openapi.IN_FORM, description="Title in Russian", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'description_ru', openapi.IN_FORM, description="Description in Russian", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'department_ru', openapi.IN_FORM, description="Department in Russian", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'image', openapi.IN_FORM, description="File to upload", type=openapi.TYPE_FILE
            ),
        ],
        responses={
            200: NewsSerializerRU,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        news = self.get_object(pk)
        data = request.data.copy()

        image = request.FILES.get('image')
        if image:
            fileapp_url = f"{settings.FILEAPP_URL}/"
            fileapp_response = requests.post(fileapp_url, files={'file': image}, data={'service': 'news'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload image.'}, status=status.HTTP_400_BAD_REQUEST)
            data['image'] = fileapp_response.json().get('file_path')

        serializer = NewsSerializerRU(news, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a news item in Russian",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        news = self.get_object(pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewsDetailViewEN(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return News.objects.get(pk=pk)
        except News.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="Get a specific news item in English",
        responses={
            200: NewsSerializerEN(),
            404: "Not Found"
        }
    )
    def get(self, request, pk):
        news = self.get_object(pk)
        serializer = NewsSerializerEN(news)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update a news item in English",
        operation_description="Update an existing news item with optional image upload in English.",
        manual_parameters=[
            openapi.Parameter(
                'title_en', openapi.IN_FORM, description="Title in English", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'description_en', openapi.IN_FORM, description="Description in English", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'department_en', openapi.IN_FORM, description="Department in English", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'image', openapi.IN_FORM, description="File to upload", type=openapi.TYPE_FILE
            ),
        ],
        responses={
            200: NewsSerializerEN,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        news = self.get_object(pk)
        data = request.data.copy()

        image = request.FILES.get('image')
        if image:
            fileapp_url = f"{settings.FILEAPP_URL}/"
            fileapp_response = requests.post(fileapp_url, files={'file': image}, data={'service': 'news'})
            if fileapp_response.status_code != 201:
                return Response({'error': 'Failed to upload image.'}, status=status.HTTP_400_BAD_REQUEST)
            data['image'] = fileapp_response.json().get('file_path')

        serializer = NewsSerializerEN(news, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a news item in English",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        news = self.get_object(pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)