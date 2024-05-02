from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Post, Tag, Author


class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Post
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

    def validate(self, value):
        caption = self.initial_data['caption']
        if caption[0] != '#':
            caption = '#' + caption
        existing_tag = Tag.objects.filter(caption=caption).exists()
        if existing_tag:
            raise serializers.ValidationError("Tag with this name already exists.")
        return value


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'

    def validate_email_address(self, value):
        last_name = self.initial_data['last_name']
        first_name = self.initial_data['first_name']
        existing_author = Author.objects.filter(
            last_name=last_name, first_name=first_name, email_address=value
        ).exists()
        if existing_author:
            raise serializers.ValidationError("Author with the same name and email already exists.")
        return value