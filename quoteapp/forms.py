from django.forms import ModelForm, CharField, TextInput, Textarea, DateField, DateInput
from .models import Tag, Quote, Author


class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=25,
                     required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):

    fullname = CharField(max_length=100, required=True, widget=TextInput())
    born_date = DateField(widget=DateInput(attrs={'type': 'date'}))
    born_location = CharField(min_length=3, max_length=50)
    description = CharField(max_length=1000)

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):

    text = CharField(widget=Textarea(attrs={'rows': 5}))

    class Meta:
        model = Quote
        fields = ['author', 'text']
        exclude = ['tags']
