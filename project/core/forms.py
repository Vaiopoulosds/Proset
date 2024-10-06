from django import forms
from .models import Book


# we create a form that will handle the CRUD operations, using the class meta we give a model = Book
# we select the fields that we want to access in that form
# we added the widgets for the date input field , cause of issues with the simple imput
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "pub_date",
            "price",
            "is_published",
            "category",
            "description",
        ]
        widgets = {
            "pub_date": forms.DateInput(attrs={"type": "date"}),
        }
