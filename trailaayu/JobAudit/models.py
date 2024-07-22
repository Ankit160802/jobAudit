from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class members(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True,blank=True)

class directory(models.Model):
    class Meta:
        managed=False
        db_table='plant_directory'

