from django.db import models

class User(models.Model):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    email           = models.CharField(max_length=100, unique=True)
    password        = models.CharField(max_length=100)
    phone_number    = models.CharField(max_length=100)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

