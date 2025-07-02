import django_filters
from .models import (
    BooksAuthor ,BooksBook,BooksBookshelf,BooksFormat ,BooksLanguage,  
    BooksSubject,BooksBookAuthors,BooksBookSubjects,BooksBookBookshelves,
    BooksBookLanguages
)

from django.db.models import Q, F, Subquery


class BookFilter(django_filters.FilterSet):
    # Book ID numbers specified as Project Gutenberg ID numbers.
    book_id = django_filters.CharFilter(
        field_name='gutenberg_id', lookup_expr='icontains', label='Project Gutenberg ID')

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title Contains')
    language = django_filters.CharFilter(method='filter_language', lookup_expr='icontains',        label='Language Code')
    author = django_filters.CharFilter(method='filter_author',label='Author Name Contains')
    topic = django_filters.CharFilter(method='filter_topic', label='Topic or Subject' )
    mime_type = django_filters.CharFilter(method='filter_mime_type',   label='Download Format (MIME Type)')

    class Meta:
        model = BooksBook
        fields = []

    def filter_language(self, queryset,name,value):
        langs = [lang.strip() for lang in value.split(",")]
        book_ids = BooksBookLanguages.objects.filter(
            language_id__in=BooksLanguage.objects.filter(
                code__in=langs
            ).values('id')
        ).values('book_id')
        return queryset.filter(id__in=Subquery(book_ids)).distinct()
    
    
    def filter_author(self, queryset, name, value):
        matched_authors = BooksAuthor.objects.filter(name__icontains=value)
        print("Matched authors:", list(
            matched_authors.values_list('id', 'name'))[:5])

        # BooksAuthor
        book_ids = BooksBookAuthors.objects.filter(
            author_id__in=BooksAuthor.objects.filter(
                name__icontains=value).values('id')
        ).values('book_id')
        print("Book IDs:", list(book_ids)[:10])
        return queryset.filter(id__in=Subquery(book_ids))

    def filter_topic(self, queryset, name, value):
        keywords = [kw.strip() for kw in value.split(",")]
        subject_book_ids_q = Q()
        bookshelf_ids_q = Q()
        for kw in keywords:
            subject_book_ids_q |= Q(name__icontains=kw)
            bookshelf_ids_q |= Q(name__icontains=kw)
            
        
        subject_book_ids = BooksBookSubjects.objects.filter(
            subject_id__in=BooksSubject.objects.filter(subject_book_ids_q).values('id')
        ).values('book_id')

        shelf_book_ids = BooksBookBookshelves.objects.filter(
            bookshelf_id__in=BooksBookshelf.objects.filter(bookshelf_ids_q).values('id')
        ).values('book_id')
        
        return queryset.filter(
            Q(id__in=Subquery(subject_book_ids)) | 
            Q(id__in=Subquery(shelf_book_ids))
        )
        

    def filter_mime_type(self, queryset, name, value):
        format_book_ids = BooksFormat.objects.filter(
            mime_type__icontains=value
        ).values('book_id')
        return queryset.filter(id__in=format_book_ids)
