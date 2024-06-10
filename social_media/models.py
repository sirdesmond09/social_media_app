from django.db import models
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    """
    Model representing a tag that can be associated with posts.
    
    Fields:
    - name: The name of the tag, which is unique and has a maximum length of 50 characters.
    - created_at: The date and time when the tag was created.
    """
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    Model representing a post created by a user.
    
    Fields:
    - author: The user who created the post.
    - content: The text content of the post.
    - likes: Users who have liked the post.
    - image: An optional image associated with the post.
    - video: An optional video associated with the post.
    - tags: Tags associated with the post.
    - created_at: The date and time when the post was created.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.content[:20]}'


class Reply(models.Model):
    """
    Model representing a reply to a post.
    
    Fields:
    - user: The user who created the reply.
    - post: The post that the reply is associated with.
    - content: The text content of the reply.
    - created_at: The date and time when the reply was created.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, related_name='replies', on_delete=models.CASCADE, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
