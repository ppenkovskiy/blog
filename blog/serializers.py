from rest_framework import serializers
from .models import Post, Tag, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = '__all__'
#
#     def validate(self, value):
#         caption = self.initial_data['caption']
#         if caption[0] != '#':
#             caption = '#' + caption
#         existing_tag = Tag.objects.filter(caption=caption).exists()
#         if existing_tag:
#             raise serializers.ValidationError("Tag with this name already exists.")
#         return value
#
#
# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'
#
#     def validate(self, value):
#         user_name = self.initial_data['user_name']
#         user_email = self.initial_data['user_email']
#         text = self.initial_data['text']
#         post = self.initial_data['post']
#
#         existing_comment = Comment.objects.filter(
#             user_name=user_name,
#             user_email=user_email,
#             text=text,
#             post=post
#         ).exists()
#
#         if existing_comment:
#             raise serializers.ValidationError("You have already submitted this comment.")
#
#         return value
