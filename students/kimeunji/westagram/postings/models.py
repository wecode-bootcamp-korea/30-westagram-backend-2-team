from django.db import models

class Posting(models.Model):
    text       = models.TextField()
    image_url  = models.URLField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    user       = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'
        
class Comment(models.Model):
    user       = models.ForeignKey("users.User", on_delete=models.CASCADE)
    posting    = models.ForeignKey("postings.Posting", on_delete=models.CASCADE)
    comment    = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'comments'