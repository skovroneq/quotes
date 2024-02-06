from django.forms import ModelForm, CharField, TextInput, Textarea
from .models import Tag, Quote, Author


class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=25,
                     required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):

    fullname = CharField(max_length=100, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname']


class QuoteForm(ModelForm):

    text = CharField(widget=Textarea(attrs={'rows': 5}))

    class Meta:
        model = Quote
        fields = ['author', 'text']
        exclude = ['tags']
