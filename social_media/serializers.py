from rest_framework import serializers
from .models import Post, Reply, Tag
from django.contrib.auth import get_user_model

User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', "created_at"]

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'content', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    replies_count = serializers.IntegerField(source='replies.count', read_only=True)
    replies = ReplySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, required=False)
    author = serializers.CharField(source='author.get_full_name', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'tags', 'likes_count', 'replies_count', 'replies', 'image', 'video', 'created_at']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            post.tags.add(tag)
        return post
