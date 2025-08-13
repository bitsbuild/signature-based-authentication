from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer,CharField,ValidationError
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_201_CREATED
from rest_framework.permissions import IsAuthenticated
class UserSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email','username','password','confirm_password']
        extra_kwargs = {
            "confirm_password":{
                "write_only":True
            }
        }
    def validate(self, attrs):
        if User.objects.filter(username=attrs['username']).exists():
            raise ValidationError(
                {
                    "Error":"Username Already In Use"
                }
                )
        elif User.objects.filter(email=attrs['email']).exists():
            raise ValidationError(
                {
                    "Error":"Account Already Exists For This Email"
                }
            )
        elif attrs['password'] != attrs['confirm_password']:
            raise ValidationError(
                {
                    "Error":"Passwords Do Not Match"
                }
            )
        else:
            return attrs
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
@api_view(['POST'])
def create(request):
    try:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(
            {
                "Status":"Account Creation Successful"
            },status=HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {
                "Status":"Account Creation Failed",
                "Error":str(e)
            },status=HTTP_400_BAD_REQUEST
        )
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request):
    try:
        request.user.delete()
        return Response(
            {
                "Status":"Account Deleted Successfully"
            },status=HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {
                "Status":"Account Deletion Failed",
                "Error":str(e)
            },status=HTTP_400_BAD_REQUEST
        )