from django.urls import path
from api.views import verify
urlpatterns = [
    path('verify/',verify,name="verify")
]
