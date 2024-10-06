from django.db import models


class Author(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=50)
    last_name = models.CharField(verbose_name="Last Name", max_length=50)
    birth_date = models.DateField(verbose_name="Birth Date")
    description = models.TextField(verbose_name="Description", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"


class Category(models.Model):
    name = models.CharField(verbose_name="Name", max_length=50, unique=True)
    description = models.TextField(verbose_name="Description", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Title", max_length=80)
    pub_date = models.DateField(verbose_name="Pub Date")
    price = models.FloatField(verbose_name="Price")
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Description", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
