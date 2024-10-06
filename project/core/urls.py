from django.urls import path
from . import views

# url pattern for the main view of the page
urlpatterns = [
    path("", views.author_list, name="author_list"),  # Task 1
    path("books-prices/", views.book_prices_list, name="books_list"),  # Task 2
    path(
        "books-categories/", views.book_categories_list, name="books_categories"
    ),  # Task 3
    path("books/", views.book_list, name="book_list"),  # Task 4, 5
    path("books/create/", views.create_book, name="create_book"),  # Task 4
    path("books/update/<int:pk>/", views.update_book, name="update_book"),  # Task 4
    path("books/delete/<int:pk>/", views.delete_book, name="delete_book"),  # Task 4
]
