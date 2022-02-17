from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=50)
    email        = models.CharField(max_length=300)
    password     = models.CharField(max_length=50)
    phone_number = models.BigIntegerField()
    
    class Meta:
        db_table = 'users'