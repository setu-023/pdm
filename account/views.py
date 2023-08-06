from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import *
from .serializers import *

class UserRegisterAPIView(APIView):
    
    def post(self, request, *args, **kwargs):

        try:
            user = User.objects.create(
                email=self.request.data['email'],
                # name=self.request.data['name']
            )          
            user.set_password(self.request.data['password'])
            user.save()
            get_token = Token.objects.create(user=user)
            serializer = UserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(data={'message': f'this field is required: {e}'}, status=status.HTTP_409_CONFLICT)


class LoginAPIView(APIView):
    

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data['email'])
            password = request.data['password']
        except Exception as e:
            return Response(data={'message': f'this field is required: {e}'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        if user.check_password(password):
                print(user)
                get_token = Token.objects.get(user=user).key
                print(get_token)
                return Response({'msg': 'successfully logged in', 'data':get_token}, status.HTTP_200_OK,)
        else:
            return Response({'msg': 'Invalid password', }, status.HTTP_405_METHOD_NOT_ALLOWED,)

