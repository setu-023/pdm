from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from document.models import Document, Metadata, Type, FileSharing
from .serializers import DocumentSerializer, MetadataSerializer, FileSharingSerializer

class Test(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        return Response({'data':'hello'})

class DocumentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.data['uploaded_by'] = request.user.id
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            ###creating metadata for file
            Metadata.objects.create(
                document = Document.objects.get(id=serializer.data['id']),
                owner = request.user,  
                format = Type.objects.get(id=serializer.data['type']).document_type    
            )
            
            return Response({'message': 'data created', 'data': serializer.data,'status':status.HTTP_201_CREATED})
        else:
            return Response({'message': 'not okay', 'data': serializer.errors, 'status':status.HTTP_409_CONFLICT})
    
    def get(self, request, format=None):
        documents = Document.objects.all()
        if documents:
            serializer = DocumentSerializer(documents, many=True).data
            return Response({'message': 'showing data', 'data': serializer,'status':status.HTTP_200_OK})
        return Response({'message': 'no data', 'data': [], 'status':status.HTTP_404_NOT_FOUND})

class DocumentRetriveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            document = Document.objects.get(id=pk)
            serializer = DocumentSerializer(document).data
            return Response({'message': 'showing data', 'data': serializer,'status':status.HTTP_200_OK})
        except:
            return Response({'message': 'no data', 'data': [], 'status':status.HTTP_404_NOT_FOUND})

    def put(self, request, pk, format=None):
        try:
            document = Document.objects.get(id=pk)
            if request.user == document.uploaded_by:
                serializer = DocumentSerializer(document, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                return Response({'message': 'showing data', 'data': serializer.data,'status':status.HTTP_200_OK})
            return Response({'message': 'user not allow', 'data': [], 'status':status.HTTP_403_FORBIDDEN})

        except:
            return Response({'message': 'no data', 'data': [], 'status':status.HTTP_404_NOT_FOUND})

    def delete(self, request, pk, format=None):
        try:
            document = Document.objects.get(id=pk)
            if request.user == document.uploaded_by:
                document.delete()
                return Response({'message': 'data deleted', 'data': [],'status':status.HTTP_200_OK})
            return Response({'message': 'user not allow', 'data': [], 'status':status.HTTP_403_FORBIDDEN})

        except:
            return Response({'message': 'no data', 'data': [], 'status':status.HTTP_404_NOT_FOUND})

class MetadataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        try:
            meta_data = Metadata.objects.get(id=pk)
            if request.user == meta_data.owner:
                # print('test')
                serializer = MetadataSerializer(meta_data, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                return Response({'message': 'showing data', 'data': serializer.data,'status':status.HTTP_200_OK})
            return Response({'message': 'user not allow', 'data': [], 'status':status.HTTP_403_FORBIDDEN})

        except Exception as e:
            print(e)
            return Response({'message': 'no data', 'data': [], 'status':status.HTTP_404_NOT_FOUND})


class FileSharingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            get_document = Document.objects.get(id=request.data['shared_document']).uploaded_by
            print(get_document)
            print(request.user)
            if get_document == request.user:
                serializer = FileSharingSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'data created', 'data': serializer.data,'status':status.HTTP_201_CREATED})
                else:
                    return Response({'message': 'not okay', 'data': serializer.errors, 'status':status.HTTP_409_CONFLICT})
            return Response({'message': 'user not allow', 'data': [], 'status':status.HTTP_409_CONFLICT})

        except Exception as e:
            return Response({'message': 'something went wrong', 'data': e, 'status':status.HTTP_409_CONFLICT})


    def get(self, request, format=None):
        get_shared_document = FileSharing.objects.filter(shared_with=request.user)
        serializer = FileSharingSerializer(get_shared_document, many=True).data
        if not serializer:            
            return Response({'message': 'no shared file', 'data': [], 'status':status.HTTP_404_NOT_FOUND})
        else:
            return Response({'message': 'showing data', 'data': serializer,'status':status.HTTP_200_OK})


class ViewFileSharingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        get_shared_document = FileSharing.objects.filter(shared_with=request.user)
        serializer = FileSharingSerializer(get_shared_document, many=True).data
        if not serializer:            
            return Response({'message': 'no shared file', 'data': [], 'status':status.HTTP_200_OK})
        else:
            return Response({'message': 'showing data', 'data': serializer,'status':status.HTTP_200_OK})


class SearchAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, **kwargs):
        q = request.GET['q']
        get_metadata = Metadata.objects.filter(owner=request.user.id)
        results = get_metadata.filter(Q(title__contains=q) | Q(description__contains=q) |
                                Q(format=q) | Q(upload_date__contains=q))
        if not results:
            return Response({'message': 'no shared file', 'data': [], 'status':status.HTTP_404_NOT_FOUND})
        serializer = MetadataSerializer(get_metadata, many=True).data
        return Response({'message': 'showing data', 'data': serializer,'status':status.HTTP_200_OK})

