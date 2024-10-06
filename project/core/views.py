from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.db.models import Avg, Min, Max, Q
from django.shortcuts import get_object_or_404, redirect, render
from .models import Book, Author, Category
from django.db.models.functions import Round
from .forms import BookForm


# we create the author view / Task 1
# we select the authors and then use the prefetch related to preload the all related books for each, for optimization
# we are ordering the prefetch related method with Prefetch, adding the queryset with order by
# and finally we are ordering by first_name , then last name each author and render them in the template
def author_list(request):
    authors = Author.objects.prefetch_related(
        Prefetch("book_set", queryset=Book.objects.order_by("title"))
    ).order_by("first_name", "last_name")

    return render(request, "authors_books.html", {"authors": authors})


# we create the book_prices_list / Task 2
# we select the authors, then use the annoate method to "create" fields for the avg, min and max price of each book
# then we only provide the values related to the task and the fields we created, then order it by first and last name
def book_prices_list(request):
    authors = (
        Author.objects.annotate(
            avg_price=Round(Avg("book__price"), 2),
            min_price=Min("book__price"),
            max_price=Max("book__price"),
        )
        .values("first_name", "last_name", "avg_price", "min_price", "max_price")
        .order_by("first_name", "last_name")
    )

    return render(request, "books_prices.html", {"authors": authors})


# we create the book categories list view / Task 3
# starting from the books we select related the category for each book and simply order the books by their title
def book_categories_list(request):
    books = Book.objects.select_related("category").order_by("title")

    return render(request, "book_categories.html", {"books": books})


# Create a list view in a table with search // Task 4,5
# we initiallize the params that will be used for the query and provide the defaults
# if the order is descenting we change the order_by part with a - in fornt
# we get the books , with selection of realted author and category
# then we use the Q object provided by django to filter the results of the query
# then we use the paginator that django provides passing the books and the items per page
# we create an object context to be pased for the template to handle
def book_list(request):
    search_query = request.GET.get("search", "")
    order_by = request.GET.get("order_by", "title")
    direction = request.GET.get("direction", "asc")
    page_number = request.GET.get("page", 1)

    if direction == "desc":
        order_by = f"-{order_by}"

    books = (
        Book.objects.select_related("author", "category")
        .filter(Q(title__icontains=search_query))
        .order_by(order_by)
    )

    paginator = Paginator(books, 20)
    page_obj = paginator.get_page(page_number)

    context = {
        "books": page_obj,
        "search_query": search_query,
        "order_by": order_by.lstrip("-"),
        "direction": direction,
        "paginator": paginator,
        "page_obj": page_obj,
    }

    return render(request, "book_list.html", context)


# This part will be used for creation of a new book
# we use the is valid form to decide if we can save the form
# if the form is valid we procceed with the save and redirection at the list
def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "book_form.html", {"form": form})


# This part will handle the updating of a book
# we need a certain pk , so we use the pk ( id ) and the get object or 404 to ensure that we have a book to update
# then we check the method
# after that it is similar with the create form
def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "book_form.html", {"form": form, "book": book})


# This part will handle the delete
# again we check if the object exists
# check the request method
# then we use the delete() method to remove the book
# and we redirect at the list
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "book_confirm_delete.html", {"book": book})
