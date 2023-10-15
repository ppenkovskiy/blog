from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=20)
    excerpt = models.CharField(max_length=100)
    image_name = models.CharField(max_length=20)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)
    content = models.CharField(max_length=1000)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

