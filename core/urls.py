from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('events/', views.events, name='events'),
    path('downloads/', views.downloads, name='downloads'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('reports/', views.public_reports, name='public_reports'),
    path('reports/<int:report_id>/view/', views.view_report, name='view_report'),
    path('reports/<int:report_id>/download/', views.download_report, name='download_report'),
    path('logout/', views.logout_view, name='logout'),
]