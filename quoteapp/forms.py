from django.forms import ModelForm, CharField, TextInput, Textarea
from .models import Tag, Quote


class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=25,
                     required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):

    text = CharField(widget=Textarea(attrs={'rows': 3}))

    class Meta:
        model = Quote
        fields = ['text']
        exclude = ['author', 'tags']
