from rest_framework import serializers
from .models import (
    BooksBook, BooksBookAuthors, BooksAuthor,
    BooksBookSubjects, BooksSubject,
    BooksBookBookshelves, BooksBookshelf,
    BooksBookLanguages, BooksLanguage,
    BooksFormat
)


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    bookshelves = serializers.SerializerMethodField()
    formats = serializers.SerializerMethodField()
    
    class Meta:
        model = BooksBook
        fields = [
            'id', 'title', 'authors',
            'genres', 'languages',
            'subjects', 'bookshelves',
            'formats'
        ]

    def get_authors(self, obj):
        author_ids = BooksBookAuthors.objects.filter(
            book_id=obj.id).values_list('author_id', flat=True)
        authors = BooksAuthor.objects.filter(id__in=author_ids)
        return [
            {
                "name": author.name,
                "birth_year": author.birth_year,
                "death_year": author.death_year
            }
            for author in authors
        ]

    def get_genres(self, obj):
        subject_ids = BooksBookSubjects.objects.filter(
            book_id=obj.id).values_list('subject_id', flat=True)
        return list(BooksSubject.objects.filter(id__in=subject_ids).values_list('name', flat=True))

    def get_languages(self, obj):
        lang_ids = BooksBookLanguages.objects.filter(
            book_id=obj.id).values_list('language_id', flat=True)
        return list(BooksLanguage.objects.filter(id__in=lang_ids).values_list('code', flat=True))

    def get_subjects(self, obj):
        subject_ids = BooksBookSubjects.objects.filter(
            book_id=obj.id).values_list('subject_id', flat=True)
        return list(BooksSubject.objects.filter(id__in=subject_ids).values_list('name', flat=True))

    def get_bookshelves(self, obj):
        shelf_ids = BooksBookBookshelves.objects.filter(
            book_id=obj.id).values_list('bookshelf_id', flat=True)
        return list(BooksBookshelf.objects.filter(id__in=shelf_ids).values_list('name', flat=True))

    def get_formats(self, obj):
        formats = BooksFormat.objects.filter(book_id=obj.id)
        return [
            {
                "mime_type": f.mime_type,
                "url": f.url
            }
            for f in formats
        ]
