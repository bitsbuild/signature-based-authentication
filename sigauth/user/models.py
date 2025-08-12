from django.db.models import Model,UUIDField,CharField,EmailField,URLField,DateTimeField
from uuid import uuid4
class User(Model):
    id = UUIDField(default=uuid4,editable=False,blank=False,null=False,primary_key=True)
    name = CharField(max_length=150,blank=False)
    username = CharField(max_length=25,unique=True,blank=False)
    password = CharField(max_length=32,blank=False)
    email = EmailField(unique=True,blank=False)
    signature = URLField(unique=True,editable=False,blank=False,null=False)
    created = DateTimeField(auto_now_add=True,editable=False,blank=False,null=False)
    updated = DateTimeField(auto_now=True,editable=False,blank=False,null=False)
    def __str__(self):
        return self.name
