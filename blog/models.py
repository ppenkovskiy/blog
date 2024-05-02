from django.db import models
from django.db.models import UniqueConstraint
from django.utils.text import slugify
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


class Tag(models.Model):
    caption = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.caption}"


class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to='posts', null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    tag = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ('date',)
        constraints = [
            UniqueConstraint(
                fields=['title', 'excerpt', 'content'],
                name='unique_post'
            )
        ]


class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
