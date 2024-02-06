from django.shortcuts import render, redirect
from .forms import TagForm, QuoteForm, AuthorForm
from .models import Tag, Quote, Author

# Create your views here.


def main(request):
    return render(request, 'quoteapp/index.html')


def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/tag.html', {'form': form})

    return render(request, 'quoteapp/tag.html', {'form': TagForm()})


def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/author.html', {'form': form})

    return render(request, 'quoteapp/author.html', {'form': AuthorForm()})


def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            new_quote = form.save(commit=False)

            selected_author = form.cleaned_data.get('author')
            new_quote.author = selected_author

            new_quote.save()

            choice_tags = Tag.objects.filter(
                name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to='quoteapp:main')
        else:
            print(request.POST)
            print(form.errors)
            return render(request, 'quoteapp/quote.html', {"authors": authors, "tags": tags, 'form': form})

    return render(request, 'quoteapp/quote.html', {"authors": authors, "tags": tags, 'form': QuoteForm()})
