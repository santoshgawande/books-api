from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import BooksBook, BooksAuthor, BooksBookAuthors
from .serializers import BookSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BooksBook.objects.all().order_by('-download_count')
    serializer_class = BookSerializer
    # Filter
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "total": self.paginator.page.paginator.count,
                "results": serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "total": len(serializer.data),
            "results": serializer.data
        })
