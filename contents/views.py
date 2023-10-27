from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import vodtest
from .serializers import vodSerializer
# GET 요청만 처리 (조회)
@api_view(['GET'])
def vodTestget(request) :
    if request.method == 'GET' :
        vods = vodtest.objects.all()
        serializer = vodSerializer(vods, many=True)
        return Response(serializer.data)
# @api_view(['GET'])
# def vodTestgetid (request) :
#     if request.method == 'GET' :
#         vod = vodtest.objects.get
#         serializer = vodSerializer(vods, many=True)
#         return Response(serializer.data)

@api_view(['POST'])
def vodTestPOST(request) :
    serializer = vodSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)