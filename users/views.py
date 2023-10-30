from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MemberSerializer
from rest_framework import status
from django.shortcuts import render
@api_view(['POST'])
def userSignup(request) :
    serializer = MemberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def simple_view(request):
    return render(request, 'users/login.html')