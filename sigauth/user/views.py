from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.serializer import UserSerializer
from rest_framework.status import HTTP_201_CREATED,HTTP_400_BAD_REQUEST
@api_view(['POST'])
def create(request):
    # Next To Do: Stored Hashed Password And Store Image To Online Storage And Store Link In Instance Here
    try:
        data = request.data
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "Status":"Account Created Successfully",
            },status=HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {
                "Status":"Error",
                "Error":str(e)
            },status=HTTP_400_BAD_REQUEST
        )
@api_view(['POST'])
def login(request):
    pass
@api_view(['POST'])
def delete(request):
    pass