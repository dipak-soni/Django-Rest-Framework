from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from .api_file.serializers import CarSerializer,CarSerializerUsingModel,ShowRoomSerializer,ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view       # for using function based rest api then this import is needed
from rest_framework import status
from rest_framework.views import APIView          # for using class based views
from rest_framework.authentication import BaseAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .api_file.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import LimitOffsetPagination
# If we are not using rest framework then our views are defined like this:
# In this method we have to write attributes names in the response that would be headache for us.
"""
def CarListView(request):
    cars=CarList.objects.all()
    data={'cars':list(cars.values())}
    return JsonResponse(data)

def CarDetailView(request,pk):
    car=CarList.objects.get(id=pk)
    data={'name':car.name,'description':car.description,'active':car.active}
    return JsonResponse(data)

"""

# using rest framework and function based views
# using serializers.serializer way
"""
@(api_view(['GET','POST']))
def CarListView(request):
    if request.method=='GET':
        car=CarList.objects.all()
        serializer=CarSerializer(car,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=400)
"""


# using rest framework and serializers.model way
@(api_view(['GET','POST']))
def CarListView(request):
    if request.method=='GET':
        car=CarList.objects.all()
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(car, request)
        serializer=CarSerializerUsingModel(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)
    elif request.method=='POST':
        serializer=CarSerializerUsingModel(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=400)
    
        


# using rest framework for another view and using serializers.serializer way
@(api_view(['GET','PUT','DELETE']))
def CarDetailView(request,pk):
    if request.method=='GET':
        try:
            car=CarList.objects.get(id=pk)
            serializer=CarSerializer(car)
            return Response(serializer.data)
        except :
            return Response(status.HTTP_404_NOT_FOUND)
    elif request.method=='PUT':
        car=CarList.objects.get(id=pk)
        serializer=CarSerializer(car,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=400)
    
    elif request.method=='DELETE':
        car=CarList.objects.get(id=pk)
        car.delete()
        return Response(status=204)


# using class based views and model serializer (preferred method)
class ShowRoomListView(APIView):
    # authentication_classes=[BaseAuthentication]
    # permission_classes=[IsAuthenticated]
    # we do not need to add add classes for authentication cause it were aleady in settings.py file
    # authentication_classes=[SessionAuthentication]
    # permission_classes=[IsAuthenticated]
    
    def get(self,request):
        showrooms=ShowRoomList.objects.all()
        serializer=ShowRoomSerializer(showrooms,many=True,context={'request': request})
        return Response(serializer.data)
    
    def post(self,request):
        serializer=ShowRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# using class based views and model serializer method
class ShowRoomDetailView(APIView):
    def get(self,request,pk):
        try:
            showroom=ShowRoomList.objects.get(id=pk)
            serializer=ShowRoomSerializer(showroom)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        try:
            showroom=ShowRoomList.objects.get(id=pk)
            serializer=ShowRoomSerializer(showroom,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,pk):
        try:
            showroom=ShowRoomList.objects.get(id=pk)
            showroom.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    


#  another concise code to handle views do not use APIVIEW 
class ReviewListView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # authentication_classes=[BaseAuthentication]
    # permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# a more concise way to create ReviewListView class
"""
class ReviewListView(generics.ListCreateAPIView):
     queryset=Review.objects.all()
     serializer_class=ReviewSerializer

"""

class ReviewDetailView(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[ReviewUserOrReadOnlyPermission]
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

# a more concise way to create ReviewDetailView class
"""
class ReviewListView(generics.RetrieveUpdateDestroyAPIView):
     queryset=Review.objects.all()
     serializer_class=ReviewSerializer

"""

# connection between viewset and router 
class ShowRoomViewSet1(viewsets.ViewSet):
      def list(self, request):
        queryset = ShowRoomList.objects.all()
        serializer = ShowRoomSerializer(queryset, many=True,context={'request': request})
        return Response(serializer.data)

      def retrieve(self, request, pk=None):
        queryset = ShowRoomList.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ShowRoomSerializer(user)
        return Response(serializer.data)
      
      def create(self,request):
          serializer=ShowRoomSerializer(data=request.data)
          if serializer.is_valid():
              serializer.save()
              return Response(serializer.data,status=status.HTTP_201_CREATED)
          else:
              return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#  use model viewset for concise code 
class ShowRoomViewSet2(viewsets.ModelViewSet):
    queryset = ShowRoomList.objects.all()
    serializer_class = ShowRoomSerializer


class ViewReviews(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(car=pk)


class CreateReviews(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    def perform_create(self,serializer):
        pk=self.kwargs['pk']
        cars=CarList.objects.get(pk=pk)
        serializer.save(car=cars)