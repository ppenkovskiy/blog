from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Post, Tag


class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Post
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Tag
        fields = '__all__'
