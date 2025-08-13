from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user.views import create,delete
urlpatterns = [
    path("create/",create,name="create"),
    path("get-token/",obtain_auth_token,name="get-token"),
    path("delete/",delete,name="delete")
]