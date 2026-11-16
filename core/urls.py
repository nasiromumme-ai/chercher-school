from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('events/', views.events, name='events'), # <-- ADDED THIS LINE
    path('logout/', views.logout_view, name='logout'),
]