from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.serializer import UserSerializer
from rest_framework.status import HTTP_201_CREATED,HTTP_400_BAD_REQUEST
@api_view(['POST'])
def create(request):
    pass
@api_view(['POST'])
def login(request):
    pass
@api_view(['POST'])
def delete(request):
    pass