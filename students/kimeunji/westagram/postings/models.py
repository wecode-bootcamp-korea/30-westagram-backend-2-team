from operator import mod
from django.db import models

class Posting(models.Model):
    text       = models.TextField()
    image_url  = models.URLField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    user       = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'