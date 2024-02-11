from .tasks import run_spider
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import TagForm, QuoteForm, AuthorForm
from .models import Tag, Quote, Author
from scrapy.crawler import CrawlerProcess
from scraper.spiders.authors_spider import AuthorsSpider
from scraper.spiders.quotes_spider import QuotesSpider


# Create your views here.


def main(request):
    quotes = Quote.objects.all()
    return render(request, 'quoteapp/index.html', {"quotes": quotes})


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/tag.html', {'form': form})

    return render(request, 'quoteapp/tag.html', {'form': TagForm()})


@login_required
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


@login_required
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


def quotes_by_tag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    quotes = Quote.objects.filter(tags=tag)
    return render(request, 'quoteapp/quotes_by_tag.html', {'tag': tag, 'quotes': quotes})


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quoteapp/author_detail.html', {"author": author})


def scrapping(request):
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.crawl(AuthorsSpider)
    process.start()
    return render(request, 'quoteapp/scrapping.html', {'message': 'The data is being scrapped'})


def scraping_status(request):
    scraping_status = "in_progress"

    return JsonResponse({'status': scraping_status})


class ScrapeView(View):
    def get(self, request):
        # Call the Celery task to start the scraping process
        run_spider.delay()

        # Return a response indicating that the scraping has started
        return HttpResponse('Scraping started!')
