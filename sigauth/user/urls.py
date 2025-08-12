from user.views import create,login,delete
from django.urls import path
urlpatterns = [
    path('create/',create,name='create'),
    path('login/',login,name='login'),
    path('delete/',delete,name='delete')
]