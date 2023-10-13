from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=20)
    excerpt = models.CharField(max_length=100)
    image_name = models.CharField(max_length=20)
    date = models.
    slug =
    content =