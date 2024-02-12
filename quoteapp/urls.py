from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag, name='tag'),
    path('author/', views.author, name='author'),
    path('quote/', views.quote, name='quote'),
    path('quotes_by_tag/<int:tag_id>/',
         views.quotes_by_tag, name='quotes_by_tag'),
    path('author/<int:author_id>', views.author_detail, name='author_detail'),
    path('scrape/', views.scrape, name='scrape'),
    path('scraping-status/', views.scraping_status, name='scraping_status'),
]
