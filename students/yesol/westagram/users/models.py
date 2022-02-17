from django.db import models

# Create your models here.
class Member(models.Model):
    name     = models.CharField(max_length=20)
    email    = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    phone    = models.CharField(max_length=30)

    class Meta:
        db_table = "members"

