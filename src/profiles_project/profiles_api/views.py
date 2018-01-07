from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

 class HelloApiView(APIView):
     """Test APIView."""

     def get(self, request, format=None):
         """Returns a list of APIView features."""

         an_apiview = [
         'Uses HTTP methods as function',
         'similar to trad django view',
         'most control over logic',
         'mapped manually to URLs'
         ]

         return Response({
         'message': 'Hello!', 
         'an_apiview': an_apiview
         })
