from django.urls import path
from .views import (
    PostListCreate,
    PostDetail,
    LikePost,
    ReplyCreate,
    TagListCreate,
    PostByTagList,
)

urlpatterns = [
    path("posts/", PostListCreate.as_view(), name="post-list-create"),
    path("posts/<int:pk>/", PostDetail.as_view(), name="post-detail"),
    path("posts/<int:pk>/like/", LikePost.as_view(), name="like-post"),
    path("posts/<int:pk>/reply/", ReplyCreate.as_view(), name="reply-create"),
    path("tags/", TagListCreate.as_view(), name="tag-list-create"),
    path("tags/<str:tag_name>/", PostByTagList.as_view(), name="post-by-tag-list"),
]
