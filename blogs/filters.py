from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from blogs.models import PostItem, Tag


class PostFilterSet(FilterSet):
    class Meta:
        model = PostItem
        fields = ['tags', 'owner']

    tags = CharFilter(field_name="tags__slug")
    owner = CharFilter(field_name="blog__owner__login")

# class TagFilterSet(FilterSet):
#     class Meta:
#         model = Tag
#         fields = [
#             'name',
#         ]
#
#     tags = CharFilter(field_name="tags__name")
