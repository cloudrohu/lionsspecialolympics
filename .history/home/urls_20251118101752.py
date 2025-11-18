# urls.py (app-level)
from django.urls import path
from .views import (
    HomeView, ProjectListView, ProjectDetailView,
    NewsListView, NewsDetailView, ContactView, DonateView
)

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('donate/', DonateView.as_view(), name='donate'),
]
