from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from document.models import Document
from .serializers import DocumentSerializer

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
