from rest_framework.serializers import ModelSerializer
from user.models import User
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password':{
                'write_only':True
            }
        }