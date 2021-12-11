from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from blogs.models import PostItem
from blogs.serializers import PostSerializer


class PostsListView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = PostItem.objects.all().order_by('views_count')
    serializer_class = PostSerializer
