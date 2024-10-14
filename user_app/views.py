from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
   if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data=dict()
        if serializer.is_valid():
           account=serializer.save()
           data['username']=account.username
           data['email']=account.email
           refresh=RefreshToken.for_user(account)
           data['token']={
                'refresh': str(refresh),
                'access': str(refresh.access_token),
           }
        else:
           data=serializer.errors
        return Response(data)
           
           


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout(request):
    if request.method =='POST':
        request.user.auth_token.delete()
        return Response({'message': 'Logout successful'}, status=200)