from rest_framework import serializers
from .models import Question, Tag, Comment


class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Question
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
            raise serializers.ValidationError("Tag with this name already exists.")   # noqa
        return value


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'

    def get_user_name(self, obj):
        return obj.user.username
