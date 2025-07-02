# books-api
This a Django REST API implementation for querying books from the Gutenberg dataset. It includes pagination, filtering, and rich API responses

## Features Implemented

- Filtering support for:

- Title (case-insensitive, partial)

- Author (case-insensitive, partial)

- Language (multi-language)

- MIME Type

- Topic: subjects OR bookshelves (case-insensitive, partial)

-  Gutenberg ID (book_id)

## Rich JSON Response per book:

- Title

- Authors (name, birth/death year)

- Subjects (topics)

- Bookshelves

- Languages

- Available formats with MIME-type and download URL
