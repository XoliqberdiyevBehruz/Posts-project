from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media/')
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=False)

    

    def __str__(self):
        return self.title
    
class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
