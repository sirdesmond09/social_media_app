from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post, Reply, Tag
from .serializers import PostSerializer, ReplySerializer, TagSerializer
from rest_framework.exceptions import NotFound

class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     "feed",
        #     {
        #         "type": "feed_message",
        #         "message": PostSerializer(post).data,
        #     }
        # )

    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', None)
        if search_query:
            self.queryset = self.queryset.filter(content__icontains=search_query)
        return super().list(request, *args, **kwargs)

class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class LikePost(generics.GenericAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     "feed",
        #     {
        #         "type": "feed_message",
        #         "message": PostSerializer(post).data,
        #     }
        # )
        return Response({'status': 'like status updated'})

class ReplyCreate(generics.CreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get_post(self):
        post_id = self.kwargs.get('pk')
        try:
            post = Post.objects.get(pk=post_id)
            return post
        except Post.DoesNotExist:
            raise NotFound(detail={"error" "Post does not exist"})

    def perform_create(self, serializer):
        post = self.get_post()
        reply = serializer.save(user=self.request.user, post=post)
        # post = reply.post
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     "feed",
        #     {
        #         "type": "feed_message",
        #         "message": PostSerializer(post).data,
        #     }
        # )

class TagListCreate(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

class PostByTagList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        return Post.objects.filter(tags__name=tag_name).order_by('-created_at')
