from django.core.management.base import BaseCommand
from core.factory import AuthorFactory, BookFactory, CategoryFactory
from django.db import transaction
from random import randint
from core.models import Book


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        with transaction.atomic():
            authors = AuthorFactory.create_batch(500)
            categories = CategoryFactory.create_batch(10)
            author_books = []

            for author in authors:
                num_books = randint(1, 8)
                author_books.extend(
                    BookFactory.build(author=author, category=categories[randint(0, 4)])
                    for _ in range(num_books)
                )
            Book.objects.bulk_create(author_books)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))
