from django.db import models
from users.models import User

class Post(models.Model):
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='posts')
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'

class Image(models.Model) :
    url  = models.URLField(max_length=2000)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')

    class Meta :
        db_table = 'images'