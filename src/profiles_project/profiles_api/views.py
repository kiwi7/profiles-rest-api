from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from . import serializers
from . import models
from . import permissions

# Create your views here.

class HelloApiView(APIView):
     """Test APIView."""

     serializer_class = serializers.HelloSerializer

     def get(self, request, format=None):
         """Returns a list of APIView features."""

         an_apiview = [
         'Uses HTTP methods as function',
         'similar to trad django view',
         'most control over logic',
         'mapped manually to URLs'
         ]

         return Response({'message': 'Hello!', 'an_apiview': an_apiview})

     def post(self, request):
         """Create a hello message with our name."""

         serializer = serializers.HelloSerializer(data=request.data)

         if serializer.is_valid():
             name = serializer.data.get('name')
             message = 'Hello {0} from APIView'.format(name)
             return Response({'message': message})
         else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     def put(self, request, pk=None):
         """Handles updates."""

         return Response({'method': 'put'})

     def patch(self, request, pk=None):
         """Patch only updates fields provided in the request."""

         return Response({'method': 'patch'})

     def delete(self, request, pk=None):
         """Deletes the object."""

         return Response({'method': 'delete'})


class HelloViewSet(viewsets.ViewSet):
     """Test API ViewSet."""#

     serializer_class = serializers.HelloSerializer

     def list(self, request):
         """Returns a list of ViewSet features."""

         a_viewset = [
         'Uses actions as functions',
         'more functionality less code',
         'automatic map to URLs'
         ]

         return Response({'message': 'Hello ViewSet!', 'a_viewset': a_viewset})

     def create(self, request):
         """Create msg."""

         serializer = serializers.HelloSerializer(data=request.data)

         if serializer.is_valid():
             name = serializer.data.get('name')
             message = 'Hello {0} from ViewSet'.format(name)
             return Response({'message': message})
         else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     def retrieve(self, request, pk=None):
         """Retrieve by id."""

         return Response({'method': 'retrieve', 'http_method': 'GET'})

     def update(self, request, pk=None):
         """Handles updates."""

         return Response({'method': 'update', 'http_method': 'PUT'})

     def partial_update(self, request, pk=None):
         """Partial update, Patch only updates fields provided in the request."""

         return Response({'method': 'partial_update', 'http_method': 'PATCH'})

     def destroy(self, request, pk=None):
         """Destroy removes an object."""

         return Response({'method': 'destroy', 'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
     """Handles creating and updating user profiles."""

     serializer_class = serializers.UserProfileSerializer
     queryset = models.UserProfile.objects.all()
     authentication_classes = (TokenAuthentication,) # tuple immutable
     permission_classes = (permissions.UpdateOwnProfile,)
     filter_backends = (filters.SearchFilter,)
     search_fields = ('name','email',)


class LoginViewSet(viewsets.ViewSet):
     """Checks email and pwd and returns auth token."""

     serializer_class = AuthTokenSerializer

     def create(self, request):
         """Use the ObtainAuthToken APIView to validate and create a token."""

         return ObtainAuthToken().post(request)

class UserProfileFeedViewSet(viewsets.ModelViewSet):
     """Handles creating and updating profile feed items."""

     authentication_classes = (TokenAuthentication,) # tuple immutable
     serializer_class = serializers.ProfileFeedItemSerializer
     queryset = models.ProfileFeedItem.objects.all()

     def perform_create(self, serializer):
         """Set the user profile to the logged in user."""

         serializer.save(user_profile=self.request.user)
