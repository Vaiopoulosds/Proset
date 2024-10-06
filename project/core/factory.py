import factory
from .models import Author, Book, Category
from faker import Faker


class UniqueNameIterator:
    def __init__(self):
        self.fake = Faker()
        self.used_words = set()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            word = self.fake.word()
            if word not in self.used_words:
                self.used_words.add(word)
                return word


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birth_date = factory.Faker("date")
    description = factory.Faker("paragraph")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Iterator(UniqueNameIterator())
    description = factory.Faker("sentence")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    author = factory.SubFactory(AuthorFactory)
    title = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    pub_date = factory.Faker("date")
    price = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    is_published = factory.Faker("boolean")
    category = factory.SubFactory(CategoryFactory)
