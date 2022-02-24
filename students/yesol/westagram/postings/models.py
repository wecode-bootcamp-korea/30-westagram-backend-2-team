from django.db import models

from users.models import Member

class Posting(models.Model):
    image_url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    class Meta:
        db_table = "postings"

class Comment(models.Model):
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    posting = models.ForeignKey("Posting", on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    class Meta:
        db_table = "comments"