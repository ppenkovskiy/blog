from django.db import models
from django.utils.text import slugify


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tag(models.Model):
    caption = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.caption}"


class Post(models.Model):
    title = models.CharField(max_length=20)
    excerpt = models.CharField(max_length=100)
    image_name = models.CharField(max_length=20)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name='posts')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True, related_name='posts')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"




