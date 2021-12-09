from rest_framework import generics
from blogs.models import PostItem
from blogs.serializers import PostSerializer


class PostsListView(generics.ListAPIView):
    queryset = PostItem.objects.all().order_by('views_count')
    serializer_class = PostSerializer
